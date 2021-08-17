from __future__ import annotations
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


class SerializableTypes(AdvancedEnum, AbbreviatedEnum):
    # all need to be strict uppercase for Parse to work
    STR = 1, str, ''
    INT = 2, int, 0
    BOOL = 3, bool, False
    FLOAT = 4, float, 0.0
    # FILE_META = 5, FileMeta, FileMeta()

    def __init__(self, _:int, constr: Callable[[str], T], default: T) -> None:
        def safeConstr(str: str) -> T:
            try:
                return constr(str)
            except ValueError:
                return default

        self.constr = safeConstr
        self.default = default
        self.type = constr

    @classmethod
    def _members(cls) -> list[SerializableTypes]:
        return list(i[1] for i in filter(lambda i: i[0].isupper(), cls.__dict__.items()))

    @classmethod
    def FromStr(cls, string: str) -> SerializableTypes | None:
        for m in cls._members():
            if string == str(m.type):
                return m
        return None

    @classmethod
    def FromType(cls, obj) -> SerializableTypes | None:
        members: list[SerializableTypes] = cls._members()
        for m in members:
            if type(obj) == m.type: return m
        return None

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
    def FromResponse(cls, response: py_Response):
        model = cls.Load(response.text)
        model.Code = response.status_code
        model.Raw = response.text
        return model

    @classmethod
    def Load(cls, serialized: bytes | str):
        model = cls()
        try:
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
            valueType = SerializableTypes.FromStr(v[TYPE])
            if valueType is None: continue
            model.__setattr__(k, valueType.constr(v.get(VALUE, '')))
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