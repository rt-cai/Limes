from __future__ import annotations
import inspect
from json.decoder import JSONDecodeError

from typing import Callable, Type, TypeVar, Tuple, Any
import typing
from requests import Response as py_Response
import json

from limes_common.models.basic import AbbreviatedEnum, AdvancedEnum


T = TypeVar('T')
U = TypeVar('U')

def _tryParse(constr: Callable[[T], U], data: dict[str, T], key: str, default: U) -> U:
    val = data.get(key)
    if val:
        return constr(val)
    else:
        return default

class PublicModel:
    def __init__(self, res: py_Response) -> None:
        self.Code = res.status_code
        self.data: dict = json.loads(res.text) if self.Code==200 else {}


class SerializableTypes:
    # all need to be strict uppercase for Parse to work
    STR = str, ''
    INT = int, 0
    BOOL = bool, False
    FLOAT = float, 0.0
    # FILE_META = 5, FileMeta, FileMeta()

    __typesMap = {}

    @classmethod
    def _members(cls) -> list[dict[str, Callable[[str], Any]]]:
        def get(c: type):
            allMap = SerializableTypes.__typesMap
            m = allMap.get(c, None)
            if m == None:
                d = {}
                for constr, default in [i[1] for i in filter(lambda i: i[0].isupper(), c.__dict__.items())]:
                    d[str(type(default))] = constr
                allMap[c] = d
                m = d
            return m
        all = []
        for c in inspect.getmro(cls):
            all.append(get(c))
            if c == SerializableTypes: break
        return all

    @classmethod
    def ConstrFromStr(cls, string: str) -> Callable | None:
        for d in cls._members():
            if string in d:
                return d[string]
        return None

    @classmethod
    def ConstrFromType(cls, obj) -> Callable | None:
        string = type(obj)
        return cls.ConstrFromStr(string)

    @classmethod
    def Types(cls) -> list[SerializableTypes]:
        return list(cls.__dict__[key] for key in filter(lambda k: k.isupper(), cls.__dict__.keys()))

class Model:
    __TYPE = 'type'
    __VALUE = 'value'

    # INHERITING CLASSES MUST SET DEFAULTS TO ALL CONSTRUCTOR PARAMATERS
    def __init__(self) -> None:
        self._jsonLoadSuccess = False
        self._parsed = False
        self.Code = 0
        self.Raw = ''

    @classmethod
    def FromResponse(cls, response: py_Response, typesDict: type[SerializableTypes]=SerializableTypes):
        model = cls.Load(response.text, typesDict)
        model.Code = response.status_code
        model.Raw = response.text
        return model

    @classmethod
    def Load(cls, serialized: bytes | str | dict, typesDict: type[SerializableTypes]=SerializableTypes):
        try:
            model = cls()
        except TypeError:
            raise TypeError('%s inheriting <Model> must have no requred paramaters in constructor' % str(cls))
        try:
            if isinstance(serialized, dict):
                d = serialized
            else:
                d = json.loads(serialized)
                model._jsonLoadSuccess = True
        except JSONDecodeError:
            return model

        TYPE = Model.__TYPE
        VALUE = Model.__VALUE
        found = False
        for k, v in d.items():
            if k.startswith('_'): continue
            if not isinstance(v, dict) or TYPE not in v: continue

            constr = typesDict.ConstrFromStr(v[TYPE])
            if constr is None: continue
            model.__setattr__(k, constr(v.get(VALUE, '')))
            found = True
        model._parsed = found
        return model

    def ToDict(self) -> dict:
        d = {}
        TYPE = Model.__TYPE
        VALUE = Model.__VALUE
        for k, v in self.__dict__.items():
            if k.startswith('_'): continue
            item = {}
            item[TYPE] = str(type(v))
            if isinstance(v, Model):
                item[VALUE] = v.ToDict()
            else:
                item[VALUE] = v
            d[k] = item
        return d