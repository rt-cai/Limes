from limes.tools.qol import T
import limes_common
from .testTools import AfterAll, Assert, BeforeAll, PrintStats, PrintTitle, Test

from limes import Limes
from limes_common import utils

def getLimes(env) -> Limes:
    return env['l']


PrintTitle(__file__)

@BeforeAll
def all(env: dict):
    env['l'] = Limes()
    return env

@Test
def login(env: dict):
    limes = getLimes(env)
    with open('../../credentials/elab.msl', 'r') as creds:
        creds = [l[:-1] for l in creds.readlines()]
        u = creds[0]
        p = creds[1]
        suc, msg = limes.Login(u, p)
        print(msg)
        Assert.Equal(suc, True)

@Test
def listProviders(env: dict):
    limes = getLimes(env)
    lst = limes.ListProviders()
    Assert.Equal(lst.Code, 200)
    Assert.Equal(len(lst.Providers) > 0, True)
    print([p.Name for p in lst.Providers])

@Test
def testCall(env: dict):
    limes = getLimes(env)
    res = limes.CallProvider('test_provider', 'sum', {'values': [3, 4, 5.5]})
    Assert.Equal(res.Code, 200)
    payload = res.ResponsePayload
    if isinstance(payload.Body, dict):
        print(payload.Code, payload.Error, payload.Body)
        Assert.Equal(payload.Body.get('result', 0), 12.5)

@Test
def testSearch(env: dict):
    limes = getLimes(env)
    res = limes.Search('guag peptide')
    Assert.Equal(res.Code, 200)
    for k, v in res.Hits.items():
        print(k, v)

@Test
def passthrough_elabStorage(env: dict):
    limes = getLimes(env)
    sid = 783963
    x = limes.GetStorage(sid)
    if x is not None:
        print(x.name)
        print([i.name for i in limes.GetFullStoragePath(sid)])
    else:
        Assert.Fail()

PrintStats()