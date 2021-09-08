import os

from numpy.lib.arraysetops import isin

from limes_common.models import elab as Models, provider
from .testTools import Assert, BeforeAll, PrintStats, PrintTitle, Test
from limes_common.connections.statics.eLab import ELabConnection
from limes_common import config

def getec(env) -> ELabConnection:
    return env['ec']

def getcred(ec: ELabConnection):
    ext = 'msl' if 'msl' in config.ELAB_URL else 'test' 
    path = '../../credentials/elab.%s' % ext
    u, p = list(line[:-1] for line in open(path, 'r').readlines()[:2])
    return u, p

PrintTitle(__file__)

@BeforeAll
def all(env: dict):
    env['ec'] = ELabConnection()
    return env

# @Test
# def elablogin_fail(env: dict):
#     ec = getec(env)
#     res = ec.Login('bad', 'login')
#     print(res.ToDict())

@Test
def elablogin(env: dict):
    ec = getec(env)
    u, p = getcred(ec)

    res = ec.Login(u, p)
    Assert.Equal(res.Code, 200)
    Assert.Equal(res.token is not None, True)

    env['f'] = res.user.firstName
    env['l'] = res.user.lastName

@Test
def elabLogin_using_generic(env: dict):
    ec = getec(env)
    u, p = getcred(ec)
    req = provider.GenericRequest('auth/user', 'post', {
        'username': u,
        'password': p
    })
    res = ec.MakeRequest(req)
    Assert.Equal(res.Code, 200)
    if isinstance(res.Body, dict):
        Assert.Equal(res.Body.get('token', None), ec._token)
    else:
        Assert.Fail

@Test
def elabSampleSearch(env: dict):
    ec = getec(env)
    s = 'guag_5fp'
    res = ec.SearchSamples(s)
    print('%s found with [%s]' % (len(res.data), s))
    Assert.Equal(len(res.data) > 0, True)
    print('example> %s: %s'% (res.data[0].name, res.data[0].sampleID))
    env['sid'] = res.data[0].sampleID
    env['sname'] = res.data[0].name

@Test
def elabGetSampleByID(env: dict):
    ec = getec(env)
    sid = env['sid']
    s: str = env['sname']
    res = ec.GetSample(sid)
    Assert.Equal(res.__dict__.get('Code', None), 200)
    Assert.Equal(res.name.lower(), s.lower())
    print(res.name)

# @Test
# def elabStorageLoad(env: dict):
#     ec = getec(env)
#     res = ec.ReloadStorages()
#     Assert.Equal(res.Code, 200)
#     Assert.Equal(len(res.data)>0, True)

@Test
def elabStorageSearch(env: dict):
    ec = getec(env)
    res = ec.SearchStorages('Fosmid')
    Assert.Equal(len(res)>0, True)
    print('sample: %s, %s' % (res[0].name, res[0].storageLayerID))
    env['slid'] = res[0].storageLayerID
    env['sname'] = res[0].name

@Test
def elabStorageGet(env: dict):
    slid = env['slid']
    ec = getec(env)
    s = ec.GetStorage(slid)
    if isinstance(s, Models.Storage):
        Assert.Equal(s.storageLayerID, slid)
        Assert.Equal(s.name, env['sname'])
        print([l.name for l in ec.GetFullStoragePath(s.storageLayerID)])
    else:
        Assert.Fail()


@Test
def elabSchema(env: dict):
    ec = getec(env)
    res = ec.GetSchema()
    Assert.Equal(res.Code, 503)
    print(res.Error)

@Test
def elabSearch(env: dict):
    ec = getec(env)
    res = ec.Search('guag 25')
    Assert.Equal(res.Code, 200)
    hsamples = res.Hits['samples']
    hstorages = res.Hits['storages']
    Assert.Equal(hsamples.DataType, str(Models.Sample))
    Assert.Equal(hstorages.DataType, str(Models.Storage))
    samples = [Models.Sample.Parse(s) for s in res.Hits['samples'].Data]
    storages = [Models.Storage.Parse(s) for s in res.Hits['storages'].Data]
    for s in samples[:3]:
        print(s.name, s.sampleID)
    for l in storages[:3]:
        print([ll.name for ll in ec.GetFullStoragePath(l.storageLayerID)])

    print(ec.GetSample(9763325).ToDict())
    
    
PrintStats()