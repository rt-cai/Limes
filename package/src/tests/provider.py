import json
from .testTools import AfterAll, Assert, BeforeAll, BeforeEach, PrintStats, Test

from limes_provider.ssh import SshConnection, Handler
from limes_common.models.network import Model, SerializableTypes, provider as Provider

@BeforeAll
def all(env: dict):
    url = 'local'
    setup = [
        'cd ~/workspace/Python/Limes/package/src/',
        'conda activate limes'
    ]
    cmd = 'python -m testProvider'
    timeout = 3
    keepAlive = 10
    con = SshConnection(url, setup, cmd, timeout, keepAlive)
    # con.AddOnResponseCallback(lambda m: print(m))
    # con.AddOnErrorCallback(lambda m: print('e>' + m))
    env['c'] = con
    return env

@BeforeEach
def setup(env: dict):
    return env

@Test
def checkStatus(env: dict):
    con: SshConnection = env['c']
    echo = 'test echo'
    stat = con.CheckStatus(echo)
    print(stat.Msg)
    Assert.Equal(stat.Online, True)
    Assert.Equal(stat.Echo, echo)

@Test
def getSchema(env: dict):
    con: SshConnection = env['c']
    # con.AddOnResponseCallback(lambda m: print(m))
    # con.AddOnErrorCallback(lambda m: print('e>' + m))
    s = con.GetSchema()
    for ser in s.Services:
        print(ser.Name)

    Assert.Equal(len(s.Services), 1)
    Assert.Equal(s.Services[0].Name, 's1')

@Test
def doJob(env: dict):
    con: SshConnection = env['c']
    # con.AddOnResponseCallback(lambda m: print(m))
    # con.AddOnErrorCallback(lambda m: print('e>' + m))
    sent = {
        'a': 1,
        'b': True,
        'c': 'request'
    }
    s = con.MakeRequest(sent)
    print(s)
    Assert.Equal(s['echo'], sent)

@AfterAll
def cleanup(env: dict):
    con: SshConnection = env['c']
    con.Dispose()

PrintStats()