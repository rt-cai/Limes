from __future__ import annotations
import sys, subprocess
from typing import Callable, Any, Union
from threading import Condition, Thread
from queue import Queue, Empty
import json
import uuid
import traceback

from . import ProviderConnection
from limes_common import config
from limes_common.models.network import Model, provider as Models
from limes_common.models.network.endpoints import ProviderEndpoint
_QUOTE = '\\q'
def Serialize(model: Model) -> str:
    return Console_Encode(json.dumps(model.ToDict()))
def Console_Encode(serial: str) -> str:
    return '"%s"' % (serial.replace('"', _QUOTE))
def Console_Decode(serial: str) -> str:
    return serial.replace(_QUOTE, '"')
# M = TypeVar('M')
# def Console_Decode(string: str, constr: Callable[[str], M]) -> M:
    # return constr(string.replace(_QUOTE, '"'))

class MessageID:
    def __init__(self, uuid: str = uuid.uuid4().hex) -> None:
        self.__uuid = uuid

    def AsHex(self):
        return self.__uuid

class _pipe:
    def __init__(self, io:subprocess.IO[bytes], lock: Condition=Condition(), q: Queue=Queue()) -> None:
        self.IO = io
        self.Lock = lock
        self.Q = q

class ConnectionFailedException(Exception):
    pass

class _sshConsole:
    def __init__(self, console: subprocess.Popen[bytes], onOut: Callable[[str], None], onErr: Callable[[str], None],
            timeout: float) -> None:
        ios = {}
        for name, io in [('in', console.stdin), ('out', console.stdout), ('err', console.stderr)]:
            if io is None:
                raise ValueError('an io is missing')
            else:
                ios[name] = io
        self._in = _pipe(ios['in'])
        self._out = _pipe(ios['out'])
        self._err = _pipe(ios['err'])
        self._onCloseLock = Condition()
        self._closed = False

        workers: list[Thread] = []
        def reader(pipe: _pipe, callback: Callable[[str], None]):
            io = iter(pipe.IO.readline, b'')
            while True:
                try:
                    line = next(io)
                except (StopIteration, ValueError):
                    break
                chunk = bytes.decode(line, encoding=config.ENCODING)
                callback(chunk)
            self.Dispose()
        workers.append(Thread(target=reader, args=[self._out, onOut]))
        workers.append(Thread(target=reader, args=[self._err, onErr]))

        def timeoutTask():
            self._onCloseLock.acquire()
            self._onCloseLock.wait(timeout)
            self._onCloseLock.release()
            self.Dispose()
        workers.append(Thread(target=timeoutTask))
            
        for w in workers:
            w.daemon = True # stop with program
            w.start()

    def IsClosed(self) -> bool:
        self._onCloseLock.acquire()
        closed = self._closed
        self._onCloseLock.release()
        return closed

    def __write(self, pipe: _pipe, statement: str):
        # msg = ' '.join([cmd] + [Console_Encode(arg) for arg in args])
        pipe.IO.write(bytes('%s\n' % (statement), encoding=config.ENCODING))

    def Send(self, statement:str):
        stdin = self._in
        stdin.Lock.acquire()
        self.__write(stdin, statement)
        stdin.IO.flush()
        stdin.Lock.release()

    def BatchSend(self, statements: list[str]):
        stdin = self._in
        stdin.Lock.acquire()
        for s in statements:
            self.__write(stdin, s)
        stdin.IO.flush()
        stdin.Lock.release()

    def Dispose(self):
        self._onCloseLock.acquire()
        if self._closed:
            self._onCloseLock.release()
            return
        self._closed = True
        self._onCloseLock.notify_all()
        self._onCloseLock.release()
        self.Send('logout')
        for p in [self._in, self._out, self._err]:
            p.Lock.acquire()
            p.IO.close()
            p.Lock.release()

class SshConnection(ProviderConnection):

    class Transaction:
        def __init__(self) -> None:
            self.Lock = Condition()
            self.Packets: Queue[str] = Queue()
            self.Errors: Queue[str] = Queue()
        
        def _sync(self, fn):
            self.Lock.acquire()
            fn()
            self.Lock.release()

        def Notify(self):
            self._sync(lambda: self.Lock.notify_all())
        
        def Wait(self, timeout: float):
            self._sync(lambda: self.Lock.wait(timeout))

    def __init__(self, url:str, setup: list[str], cmd: str, transactionTimeout:float, keepAliveTime:float) -> None:
        super().__init__()
        self._transactions: dict[str, SshConnection.Transaction] = {}
        self._transactionTimeout = transactionTimeout
        self._keepAliveTime = keepAliveTime
        self._url = url
        self._setup = setup
        self._cmd = cmd
        self.__connection = self._getCon()

        self._onResponseSubscribers = []
        self._onErrorSubScribers = []

    def _getCon(self) -> _sshConsole:
        cmd = ['ssh', '-tt', self._url]
        # print(cmd)
        p = subprocess.Popen(cmd,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE)
                    # time.sleep(2)
        setup = self._setup
        
        def onOut(msg):
            for cb in self._onResponseSubscribers:
                cb(msg)

            if msg.startswith(Handler.SEND_FLAG):
                msg = msg[len(Handler.SEND_FLAG):]
                parsed = Models.Message.Load(msg)
                if parsed.MessageID in self._transactions:
                    tr = self._transactions[parsed.MessageID]
                    if parsed.IsError:
                        print('provider error: %s' % parsed.Body)
                    else:
                        tr.Packets.put(parsed.Body)
                        tr.Notify()
                else:
                    print('unregistered message: %s'%msg)

        def onErr(msg):
            for cb in self._onErrorSubScribers:
                cb(msg)

            if not msg.startswith('Connection to') and not msg.endswith('closed.'):
                print('Fatal error> ' + msg)

        con = _sshConsole(p, onOut, onErr, self._keepAliveTime)
        con.BatchSend(setup)
        return con

    def _send(self, ep:ProviderEndpoint, model: Model|None = None) -> MessageID:
        if self.__connection.IsClosed():
            self.__connection = self._getCon()

        cmd = self._cmd
        mid = MessageID()
        ser = Console_Encode(json.dumps(model.ToDict())) if model is not None else ''
        statement = '%s %s %s %s' % (cmd, mid.AsHex(), ep.Path, ser)
        self.__connection.Send(statement)
        return mid

    def _listenFor(self, mid: MessageID, timeout:float=0) -> tuple[bool, str]:
        if timeout==0:
            timeout = self._transactionTimeout
        tr = SshConnection.Transaction()
        self._transactions[mid.AsHex()] = tr
        tr.Wait(timeout)
        try:
            return True, tr.Packets.get_nowait()
        except Empty:
            return False, ''

    def _makeTransaction(self, ep: ProviderEndpoint, body: Model|None = None) -> tuple[bool, str]:
        mid = self._send(ep, body)
        return self._listenFor(mid)

    def AddOnResponseCallback(self, fn: Callable[[str], None]) -> None:
        self._onResponseSubscribers.append(fn)

    def AddOnErrorCallback(self, fn: Callable[[str], None]) -> None:
        self._onErrorSubScribers.append(fn)

    def RemoveOnResponseCallback(self, fn: Callable[[str], None]) -> None:
        self._onResponseSubscribers.remove(fn)

    def RemoveOnErrorCallback(self, fn: Callable[[str], None]) -> None:
        self._onResponseSubscribers.remove(fn)

    def CheckStatus(self, echo: str) -> Models.Status.Response:
        success, res = self._makeTransaction(ProviderEndpoint.CHECK_STATUS, Models.Status.Request(echo))
        if success:
            return Models.Status.Response.Load(res)
        else:
            return Models.Status.Response(False, res)

    def GetSchema(self) -> Models.Schema:
        success, res = self._makeTransaction(ProviderEndpoint.GET_SCHEMA)
        if success:
            return Models.Schema.Load(res)
        else:
            return Models.Schema()

    def MakeRequest(self, request: dict[str, Any], typesDict: type[Models.ProviderSerializableTypes]=None) -> dict[str, Any]:
        success, res = self._makeTransaction(ProviderEndpoint.MAKE_REQUEST, Models.Generic(request))
        if success:
            if typesDict is None:
                typesDict = Models.ProviderSerializableTypes
            resModel = Models.Generic.Load(res, typesDict)
            return resModel.Dict
        else:
            return {'fatal error': 'request failed'}

    def Dispose(self):
        self.__connection.Dispose()

class Handler:
    SEND_FLAG = 'From Handler > '
    def __init__(self) -> None:
        self._lastRawRequest = ''

    def HandleCommandLineRequest(self) -> None:
        self._lastRawRequest = sys.argv
        if len(sys.argv) == 4:
            mid, endpoint, body = sys.argv[1:]
        else:
            mid, endpoint = sys.argv[1:]
            body = '{}'
        mid = MessageID(mid)
        body = Console_Decode(body)

        def toKey(k: ProviderEndpoint):
            return k.Path.title()
        knowns = {
            toKey(ProviderEndpoint.CHECK_STATUS): lambda f: lambda r: f(Models.Status.Request.Load(r)),
            toKey(ProviderEndpoint.GET_SCHEMA): lambda f: lambda r: f(),
            toKey(ProviderEndpoint.MAKE_REQUEST): lambda f: lambda r: f(Models.Generic.Load(r).Dict)
        }

        def getHandlerMethod():
            for ep in ProviderEndpoint:
                if ep.Path != endpoint: continue
                path = ep.Path.title()
                method = 'On%sRequest' % path
                myMethods = [m for m in dir(self) if m.startswith('On')]
                for m in myMethods:
                    if method == m:
                        f = getattr(self, m)
                        return knowns.get(path, lambda f: lambda r: f(r))(f)
                return None
            return None
        handler = getHandlerMethod()

        if handler is None:
            self._send(mid, 'Unrecognized endpoint [%s]' % (endpoint))
        else:
            try:
                res = handler(body)
                self._send(mid, json.dumps(res.ToDict()))
            except Exception as e:
                self._send(mid, '\n%sendpoint: %s'%(str(traceback.format_exc()), endpoint), True)
        pass

    def _send(self, mid: MessageID, msg: str, isError:bool = False):
        serialized = json.dumps(Models.Message(mid.AsHex(), msg, isError).ToDict())
        print(Handler.SEND_FLAG + serialized)

    def OnStatusRequest(self, req: Models.Status.Request) -> Models.Status.Response:
        return Models.Status.Response(False, req.Msg, 'This is an abstract Provider and must be implemented')

    def OnSchemaRequest(self) -> Models.Schema:
        return Models.Schema([
            Models.Service('Abstract service example (provider did not implement schema request)', {'a': str, 'b': bool}, {'x': int})
        ])

    def OnGenericRequest(self, req: dict) -> Models.Generic:
        return Models.Generic({
            'error': 'provider not implemented!',
            'echo': req
        })
    
