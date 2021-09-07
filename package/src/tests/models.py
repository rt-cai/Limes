from __future__ import annotations
import json

from tests.testTools import Assert, BeforeAll, PrintStats, PrintTitle, Test
from limes_common.models import Model, Primitive, SerializableTypes, provider, server

PrintTitle(__file__)

@BeforeAll
def all(env: dict):
    return env

class Inner(Model):
    a: int
    b: bool

    def __init__(self) -> None:
        # this prevents <Outer> from being registered as a <Model>
        pass

class Outer(Model):
    P: Primitive
    Dic: dict[str, Inner]
    L: list[Inner]
    B: bool
    S: str
    I: Inner
    GetTypesDict = lambda: TestTypesDict # this is useful for non-Model types
class TestTypesDict(SerializableTypes):
    # parser fn, type
    INNER = Inner.Parse, Inner
    OUTER = Outer.Parse, Outer

@Test
def modelToDict(env: dict):

    actual = Outer()
    i = actual.I = Inner()
    i.a, i.b = 11, True

    actual.P = {
        'prim': 1
    }
    p = actual.P
    d = actual.Dic = {
        'in': i 
    }
    l = actual.L = [
        i
    ]
    b = actual.B = True
    s = actual.S = 'string'
    expected = {'I': i.ToDict(), 'P': p, 'Dic': {'in': i.ToDict()}, 'L': [i.ToDict()], 'B': b, 'S': s}
    
    Assert.Equal(str(actual.ToDict()), str(expected))

@Test
def modelLoad(env: dict):
    expected = Outer()
    i = expected.I = Inner()
    i.a, i.b = 11, True

    expected.P = {
        'prim': 1, 
        'more': True,
        'strings': 'ssssss',
        'l': [
            {'nest': {'x': [{'b':'B'}, {'a': 'A'}]}},
            4
        ]
    }
    p = expected.P
    d = expected.Dic = {
        'in': i 
    }
    l = expected.L = [
        i
    ]
    b = expected.B = True
    s = expected.S = 'string'
    serial = """{"I": {"a": 11, "b": true},
        "P": {"prim": 1, "more": true, "strings": "ssssss", "l": [
            {"nest": {"x": [{"b": "B"}, {"a": "A"}]}}, 4
        ]},
        "Dic": {"in": {"a": 11, "b": true}},
        "L": [{"a": 11, "b": true}],
        "B": true,
        "S": "string"}
    """

    actual = Outer.Parse(serial)
    for i in range(len(actual.L)):
        ac = actual.L[i]
        Assert.Equal(str(type(ac)), str(Inner))

    actial_d  = actual.ToDict()
    for k, v in json.loads(serial).items():
        Assert.Equal(k in actial_d, True)
        Assert.Equal(actial_d[k], v)

class X(Model):
    d: dict
    
@Test
def arbitraryDictSerialize(env: dict):
    x = X()
    expected = x.d = {
        'a': 1,
        'b': [
            'a', 1, False
        ]
    }

    actual = x.ToDict()
    Assert.Equal(actual['d'], expected)

@Test
def arbitraryDictParse(env: dict):
    ser = {
        'd': {
            'a': 1,
            'b': [
                'a', 1, False
            ]
        }
    }

    actual = X.Parse(ser)
    Assert.Equal(actual.d, ser['d'])

@Test
def serviceSchema(env: dict):
    ser = provider.Service()
    ep = ser.Endpoint = 'asdf'
    i = ser.Input = {
        'o1': {
            'i1': bool,
            'i2': int,
            'i3': Outer
        },
        'o2': str
    }

    i_expect = ser.Input = {
        'o1': {
            'i1': str(bool),
            'i2': str(int),
            'i3': str(Outer)
        },
        'o2': str(str)
    }

    y = provider.Service.Parse(ser.ToDict())
    # print(ser.Input)
    Assert.Equal(y.Input, i_expect)

@Test
def typesDict_should_inherit_through_model(env: dict):
    lr = server.List.Response()

    p1 = server.ProviderInfo()
    p1.Name = 'test1'
    p1.Schema = provider.Schema([
        provider.Service('ep1', {'a': int, 'b': bool}, {'res': str}),
        provider.Service('ep2', {'c': int, 'd': bool}, {'res2': str})
    ])

    p2 = server.ProviderInfo()
    p2.Name = 'test2'
    p2.Schema = provider.Schema([
        provider.Service('tt1', {'x1': str}, {'res': str}),
        provider.Service('tt2', {'x2': str}, {'res2': list})
    ])

    lr.Providers = [p1, p2]
    actual = server.List.Response.Parse(lr.ToDict())
    expected = lr
    
    Assert.Equal(len(actual.Providers), len(expected.Providers))
    for i in range(len(expected.Providers)):
        ac = actual.Providers[i]
        ex = expected.Providers[i]
        Assert.Equal(ac.Name, ex.Name)
        Assert.Equal(len(ac.Schema.Services), len(ex.Schema.Services))
        for j in range(len(ex.Schema.Services)):
            Assert.Equal(ac.Schema.Services[j].Endpoint, ex.Schema.Services[j].Endpoint)

@Test
def int_float_ambiguity(env: dict):
    class Holder(Model):
        I: int
        F: float

    h = Holder()
    h.I = 1
    h.F = 1.0

    actual = Holder.Parse(h.ToDict())
    Assert.Equal(str(type(actual.I)), str(int))
    Assert.Equal(str(type(actual.F)), str(float))
PrintStats()