from __future__ import annotations
from typing import Union

from . import Model, Primitive

DataSchema = Union[str, dict]
class Service(Model):
    Endpoint: str
    Input: DataSchema
    Output: DataSchema
    def __init__(self, endpoint: str='', input: DataSchema={}, output: DataSchema={}) -> None:
        super().__init__()
        self.Endpoint = endpoint
        self.Input = input
        self.Output = output

class Schema(Model):
    Services: list[Service]
    def __init__(self, services: list[Service]=[]) -> None:
        super().__init__()
        self.Services = services
    
class ProviderRequest(Model):
    _TargetEndpoint: str
    _Method: str

    def __init__(self, endpoint: str='', method: str='') -> None:
        super().__init__()
        self._TargetEndpoint = endpoint
        self._Method = method


class GenericRequest(ProviderRequest):
    Body: Primitive

    def __init__(self, endpoint: str='', body: Primitive={}) -> None:
        super().__init__()
        self.Body = body
        self._TargetEndpoint = endpoint

class ProviderResponse(Model):
    Code: int
    Error: str

class GenericResponse(ProviderResponse):
    Body: Primitive

    def __init__(self, body: Primitive={}, code: int=200, error: str='') -> None:
        super().__init__()
        self.Body = body
        self.Code = code
        self.Error = error

class Transaction:
    class Request(ProviderRequest):
        pass

    class Response(ProviderResponse):
        pass