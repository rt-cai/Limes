from .testTools import AfterAll, Assert, BeforeAll, PrintStats, PrintTitle, Test
from limes_common.connections.ssh import SshConnection
from limes_common.models import Model, Primitive, provider as Models

PrintTitle(__file__)

@BeforeAll
def all(env: dict):
    url = 'local'
    setup = [
        'cd ~/workspace/Python/Limes/package/src/',
        'conda activate limes'
    ]
    cmd = 'python -m test_provider'
    timeout = 3
    keepAlive = 10
    con = SshConnection(url, setup, cmd, timeout, keepAlive)
    # con.AddOnResponseCallback(lambda m: print(m))
    # con.AddOnErrorCallback(lambda m: print('e>' + m))
    env['c'] = con
    return env

@Test
def getSchema(env: dict):
    con: SshConnection = env['c']
    # con.AddOnResponseCallback(lambda m: print(m))
    # con.AddOnErrorCallback(lambda m: print('e>' + m))
    s = con.GetSchema()
    Assert.Equal(s.Code, 200)

    for ser in s.Services:
        print(ser.Endpoint, ser.Input, ser.Output)

    expectedServices = ['sum', 'echo', 'say hi'] 
    for i in range(len(expectedServices)):
        actual = s.Services[i].Endpoint
        expcted = expectedServices[i]
        Assert.Equal(actual, expcted)

@Test
def testEcho(env: dict):
    con: SshConnection = env['c']
    # con.AddOnResponseCallback(lambda m: print(m))
    # con.AddOnErrorCallback(lambda m: print('e>' + m))
    sent: Primitive = {
        'message': {
            'a': 1,
            'b': True,
            'c': 'request'
        }
    }

    res = con.MakeRequest(Models.GenericRequest('echo', body=sent))
    if res.Code != 200:
        print(res.Error)
    Assert.Equal(res.Code, 200)
    data = res.Body
    if isinstance(data, dict):
        print(data)
        Assert.Equal(data['echo'], sent['message'])
    else:
        Assert.Fail()

@Test
def testOp(env: dict):
    con: SshConnection = env['c']
    # con.AddOnResponseCallback(lambda m: print(m))
    # con.AddOnErrorCallback(lambda m: print('e>' + m))
    sent: Primitive = {
        'values': [1, 2, 3.3]
    }
    res = con.MakeRequest(Models.GenericRequest('sum', body=sent))
    if res.Code != 200:
        print(res.Error)
    Assert.Equal(res.Code, 200)
    data = res.Body
    if isinstance(data, dict):
        print(data)
        Assert.Equal(data['result'], 6.3)
    else:
        Assert.Fail()

@Test
def testSearch(env: dict):
    con: SshConnection = env['c']
    r = con.Search('tol')
    print('%s results for tol' % len(r.Hits))


@AfterAll
def cleanup(env: dict):
    con: SshConnection = env['c']
    con.Dispose()

PrintStats()