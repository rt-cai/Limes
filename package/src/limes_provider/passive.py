from __future__ import annotations
import sys, subprocess, time, inspect
from typing import Callable, Tuple, TypeVar
import asyncio
import websockets
import json
from threading import Thread, Lock
from queue import Queue, Empty

from . import ProviderConnection
from limes_common import config, utils
from limes_common.models.basic import AbbreviatedEnum
from limes_common.models.network import provider as Models

_QUOTE = '[\\q]'
def Serialize(model: Models.Model) -> str:
    return Encode(json.dumps(model.ToDict()))
def Encode(serial: str) -> str:
    return '"%s"' % (serial.replace('"', _QUOTE))
M = TypeVar('M')
def Decode(string: str, constr: Callable[[str], M]) -> M:
    return constr(string.replace(_QUOTE, '"'))

class ConnectionStatus(AbbreviatedEnum):
    OK = 1
    ERR = 2
    CLOSED = 3

class Connection:
    def __init__(self, stdin: subprocess.IO[bytes], stdout: subprocess.IO[bytes],
            stderr: subprocess.IO[bytes], setup: list[str], cmd: str) -> None:
        self._stdin = stdin
        self._stdout = stdout
        self._stderr = stderr
        self.__cmd = cmd
        self._lock = Lock()
        self.Closed = False
        self._outQueue = Queue()
        self._errQueue = Queue()
        TIMEOUT = 3

        for step in setup:
            self._do(stdin, step)

        workers: list[Thread] = []
        def reader(out: subprocess.IO[bytes], q: Queue):
            # while True:
            for line in iter(out.readline, b''):
                q.put(line)
            print('todo: can end things here!!!')
            out.close()
        workers.append(Thread(target=reader, args=(stdout, self._outQueue)))
        workers.append(Thread(target=reader, args=(stderr, self._errQueue)))

        def timeoutTask():
            time.sleep(TIMEOUT)
            self._lock.acquire()
            stdin.close()
            self.Closed = True
            self._lock.release()
        workers.append(Thread(target=timeoutTask))

        for w in workers:
            w.daemon = True # thread dies with the program
            w.start()

    def _do(self, stdin: subprocess.IO[bytes], serialized: str):
        stdin.write(bytes('%s\n' % (serialized), encoding=config.ENCODING))
        stdin.flush()

    T = TypeVar('T')
    def Send(self, model: Models.Model, constr: Callable[[bytes], T]) -> Tuple[ConnectionStatus, T|str]:
        self._lock.acquire()
        status, response = self.__doSend(model, constr)
        self._lock.release()
        return status, response

    def __doSend(self, model: Models.Model, constr: Callable[[bytes], T]) -> Tuple[ConnectionStatus, T|str]:
        if self.Closed:
            return ConnectionStatus.CLOSED, 'connection timed out'
        self._do(self._stdin, '%s %s %s' % (self.__cmd, Encode(str(type(model))), Serialize(model)))
        return ConnectionStatus.OK, 'hmmm'
    
    # hmm
    def _testRead(self):
        start = utils.current_milli_time()
        while True:
            e = 0
            try:
                res = self._outQueue.get_nowait()
                print(bytes.decode(res, config.ENCODING), end='')
            except Empty:
                e += 1
            if e == 1:
                time.sleep(1)
            now = utils.current_milli_time()
            if now - start > 3000:
                break

    def _testErr(self):
        start = utils.current_milli_time()
        while True:
            e = 0
            try:
                res = self._errQueue.get_nowait()
                print(res)
            except Empty:
                e += 1
            if e == 1:
                time.sleep(1)
            now = utils.current_milli_time()
            if now - start > 3000:
                break

class ConnectionFailedException(Exception):
    pass

class PassiveConnection(ProviderConnection):
    def __init__(self, name:str, recieveUrl: str, recievePort:int) -> None:
        super().__init__(name)
        self.__connection = self.__open()

    def __open(self) -> Connection:
        cmd = ['ssh', '-tt', 'local']
        # print(cmd)
        p = subprocess.Popen(cmd,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE)

        # time.sleep(2)
        setup = ['cd ~/workspace/Python/Limes/package/src', 'conda activate limes']
        providerRunCmd = 'python -m fosDB'
        if p.stdin is None:
            raise ConnectionFailedException('no stdin')
        elif p.stdout is None:
            raise ConnectionFailedException('no stdout')
        elif p.stderr is None:
            raise ConnectionFailedException('no stderr')
        return Connection(p.stdin, p.stdout, p.stderr,  setup, providerRunCmd)

    def _getCon(self) -> Connection:
        if self.__connection.Closed:
            return self.__open()
        else:
            return self.__connection

    def CheckStatus(self) -> Models.Status.Response:
        # status, res = self._getCon().Send(CheckStatus.Request('asdf'), CheckStatus.Request.Load)

        con = self._getCon()
        # con._do(con._stdin, './run.sh -f')
        con.Send(Models.Status.Request('asdf'), Models.Status.Request.Load)
        con.Send(Models.Status.Request('two'), Models.Status.Request.Load)
        con._testRead()
        con._testErr()
        # print(status, res)
        return Models.Status.Response(False, 'not implimented yet')

class Handler:
    SEND_FLAG = 'From Handler > '

    def HandleCommandLineRequest(self) -> None:
        # print('===============')
        # print(len(sys.argv))
        reqType, reqBody = sys.argv[1:]
        flag = '.network.provider.'
        start = reqType.index(flag) + len(flag)
        reqType = reqType[start:-2]
        # print(type(Models))
        # print(reqType)
        def getModel():
            for n, o in inspect.getmembers(Models):
                if inspect.isclass(o) and reqType.startswith(n):
                    return n
            return None
        def getMethod(model: str | None):
            if model is None: return None
            myMethods = [m for m in dir(self) if m.startswith('On')]
            for m in myMethods:
                if model == m.replace('On', '').replace('Request', ''):
                    return getattr(self, m)
            return None

        handlerFn = getMethod(getModel())
        if handlerFn is not None:
            m = Decode(reqBody, Models.Status.Request.Load)
            # print(m.__dict__)
            res: Models.Model = handlerFn(m)
            self._send('%s, %s' % (type(res), Serialize(res)))
        # print('>>> hander done')
        pass

    def _send(self, msg):
        print(Handler.SEND_FLAG + msg)

    def OnStatusRequest(self, req: Models.Status.Request) -> Models.Status.Response:
        return Models.Status.Response(False, req.Msg, 'yo')
