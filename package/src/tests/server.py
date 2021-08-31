import os

from .testTools import Assert, BeforeAll, PrintStats, PrintTitle, Test
from limes_common.connections.statics import ServerConnection
from limes_common.models import server
from limes_common import config

def getserv(env) -> ServerConnection:
    return env['serv']

PrintTitle(__file__)

@BeforeAll
def all(env: dict):
    env['serv'] = ServerConnection()
    return env

@Test
def serverLogin(env: dict):
    ext = 'msl' if 'msl' in config.ELAB_URL else 'test' 
    path = '../../credentials/elab.%s' % ext
    tok = list(line[:-1] for line in open(path, 'r').readlines())[2]
    serv = getserv(env)
    # res = serv.Send(
    #     server.Login.Request(tok, 'test_FN', 'test_LN'),
    #     server.Login.Response.Parse,
    # )

    # if isinstance(res, ErrorModel):
    #     Assert.Fail(res.Message)

    # Assert.Equal(res.Success, True)

PrintStats()