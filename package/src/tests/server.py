import os

from numpy.lib.arraysetops import isin

from .testTools import Assert, BeforeAll, PrintStats, PrintTitle, Test
from limes_common.connections.statics.server import ServerConnection
from limes_common.models import server
from limes_common import config

def getserv(env) -> ServerConnection:
    return env['serv']

PrintTitle(__file__)

@BeforeAll
def all(env: dict):
    env['serv'] = ServerConnection()
    return env

# @Test
# def serverAuthenticate_pre(env: dict):
#     serv = getserv(env)
#     res = serv.Authenticate()
#     Assert.Equal(res.Code, 200)
#     Assert.Equal(res.Success, False)

@Test
def serverLogin(env: dict):
    ext = 'msl' if 'msl' in config.ELAB_URL else 'test' 
    path = '../../credentials/elab.%s' % ext
    u, p, _ = list(map(lambda l: l.replace('\n', ''), open(path, 'r').readlines()))
    serv = getserv(env)
    res = serv.Login(u, p)

    Assert.Equal(res.Code, 200)
    env['name'] = (res.FirstName, res.LastName)
    Assert.Equal(res.Success, True)

@Test
def serverAuthenticate(env: dict):
    serv = getserv(env)
    fn, ln = env.get('name', ('not', 'logged in'))
    res = serv.Authenticate()
    Assert.Equal(res.Code, 200)
    Assert.Equal(res.FirstName, fn)
    Assert.Equal(res.LastName, ln)
    Assert.Equal(res.Token is not None, True)


@Test
def serverList(env: dict):
    serv = getserv(env)
    res = serv.List()

    Assert.Equal(res.Code, 200)
    Assert.Equal(len(res.Providers) > 0, True)
    for p in res.Providers:
        print(p.Name)
        for s in p.Schema.Services:
            print(s.Endpoint, s.Input, s.Output)

# @Test
# def serverReloadProviders(env: dict):
#     serv = getserv(env)
#     res = serv.ReloadProviders()
#     Assert.Equal(res.Code, 200)
#     Assert.Equal(len(res.Providers) > 0, True)
#     for p in res.Providers:
#         print(p.Name)
#         for s in p.Schema.Services:
#             print(s.Endpoint, s.Input, s.Output)

# @Test
# def serverReloadCache(env: dict):
#     serv = getserv(env)
#     res = serv.ReloadCache()
#     Assert.Equal(res.Code, 200)

# @Test
# def serverSearch(env: dict):
#     serv = getserv(env)
#     x = serv.Search('benz')
#     Assert.Equal(isinstance(x.Hits, dict), True)
#     for k, v in x.Hits.items():
#         print(k, v.DataType)
#         print(v.Data[0])
#         break

# @Test
# def serverCallProvider(env: dict):
#     serv = getserv(env)
#     res = serv.CallProvider('test_provider', 'sum', {'values': [1, 2, 3.3]})
#     Assert.Equal(res.Code, 200)
#     res = res.ResponsePayload.Body
#     if isinstance(res, dict):
#         print(res)
#         Assert.Equal(res.get('result', 0), 6.3)
#     else:
#         Assert.Fail()
PrintStats()