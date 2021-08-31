import os

from limes_common.models.elab import Login
from .testTools import Assert, BeforeAll, PrintStats, PrintTitle, Test
from limes_common.connections.statics import ELabConnection
from limes_common import config

def getec(env) -> ELabConnection:
    return env['ec']

PrintTitle(__file__)

@BeforeAll
def all(env: dict):
    env['ec'] = ELabConnection()
    return env

@Test
def elablogin(env: dict):
    ec = getec(env)
    ext = 'msl' if 'msl' in config.ELAB_URL else 'test' 
    path = '../../credentials/elab.%s' % ext
    u, p = list(line[:-1] for line in open(path, 'r').readlines()[:2])
    
    res = ec.Login(u, p)
    env['f'] = res.FirstName
    env['l'] = res.LastName
    Assert.Equal(res.Code, 200)
    if res.Token is None or res.Token == '':
        Assert.Fail()

PrintStats()