from limes.tools.qol import T
from .testTools import AfterAll, Assert, BeforeAll, PrintStats, Test

from limes import Limes
from limes_common import utils

def getLimes(env) -> Limes:
    return env['l']

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
        x = limes.Login(u, p)
        Assert.Equal(x, True)

@Test
def listProviders(env: dict):
    limes = getLimes(env)
    lst = limes.ListProviders()
    if lst is not None:
        for p in lst.Providers:
            print('%s, last used: %s' %(p.Name, utils.format_from_utc(p.LastUse)))
    else:
        Assert.Fail()


# @Test
# def testSearch(env: dict):
#     limes = getLimes(env)
#     pass

PrintStats()