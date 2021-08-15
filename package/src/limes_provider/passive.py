import subprocess
import time
from typing import Tuple
import asyncio
import websockets

from . import ProviderConnection, Result
from limes_common import config, utils

class PassiveConnection(ProviderConnection):
    def __init__(self, name:str) -> None:
        super().__init__(name)
        
        once = True
        async def echo(websocket, path):
            async for message in websocket:
                print(message)
                nonlocal once
                if message == 'Begin':
                    once = True
                if once:
                    await asyncio.sleep(1)
                    await websocket.send(message)
                once = False

        loop = asyncio.get_event_loop()
        task = (lambda ws: ws.serve(echo, "localhost", 8765))(websockets) # circumvent pylance type checking error
        try:
            loop.run_until_complete(task)
            loop.run_forever()
        except asyncio.CancelledError:
            print('stopped')

    # todo: batch if need to send many >> transactions
    def _execute(self, cmd: str) -> Tuple[bool, str]:
        print(cmd)
        p = subprocess.run(cmd, capture_output=True, shell=True)
        def dec(std):
            txt = '%s' % std.decode(config.ENCODING)
            return txt
        out = dec(p.stdout)
        err = dec(p.stderr)
        success = err != ''
        return (success, out if success else err)

    def Available(self) -> Result:
        return Result(False, 'not implimented yet')

    def CheckStatus(self) -> Result:
        return Result(False, 'not implimented yet')

    def DataBySample(self, sampleId: str) -> Result:
        return Result(False, 'not implimented yet')

class Handler:
    def Handle(self, x):
        return 'hh'

# backwards, this needs to be on all the time
def ListenAsProvider(uri: str, handler: Handler, timeout: int = 10):
    async def work():
        async with (lambda ws: ws.connect(uri))(websockets) as websocket: # circumvent pylance type checking error
            await websocket.send("Begin")
            while True:
                x = await websocket.recv()
                nonlocal last
                last = utils.current_milli_time()
                print('pp' + x)
                await websocket.send(handler.Handle(x))

    last = utils.current_milli_time()
    def tryCancel():
        now = utils.current_milli_time()
        if now - last >= timeout * 1000:
            task.cancel()
        else:
            loop.call_later(timeout, tryCancel)
        print(now - last)

    loop = asyncio.get_event_loop()
    loop.call_later(timeout, tryCancel)
    task = loop.create_task(work())
    try:
        loop.run_until_complete(task)
    except asyncio.CancelledError:
        print('stopped')