from __future__ import annotations
from limes_common.models.basic import AbbreviatedEnum

from limes_common.models.network import provider as Providers
# from io import BufferedReader
# import json
# from typing import Any, overload
# from requests import Response as py_Response

# from limes_common import config
# from limes_common.connections import eLab
# from limes_common.models.basic import AbbreviatedEnum
# from . import _tryParse, ResponseModel
from . import Model, SerializableTypes, Primitive

class TransctionSet:
    class Request(Model):
        pass

    class Response(Model):
        pass

class Init(TransctionSet):
    class Response(Model):
        def __init__(self, token: str = '') -> None:
            super().__init__()
            self.CsrfToken = token

# class Init:
#     @classmethod
#     def MakeResponse(cls, csrfToken: str):
#         return {config.CSRF_NAME: csrfToken}

#     class Response(ResponseModel):
#         def __init__(self, res: py_Response) -> None:
#             super().__init__(res)
#             if self.Code == 200:
#                 try:
#                     self.Csrf = json.loads(res.text)[config.CSRF_NAME]
#                 except:
#                     self.Csrf = ''

class ServerRequestModel(Model):
    def __init__(self) -> None:
        super().__init__()
        self.ClientId = ''

class Authenticate:
    class Request(ServerRequestModel):
        def __init__(self, clientId: str = '') -> None:
            super().__init__()
            self.ClientId = clientId

    class Response(Model):
        def __init__(self, success: bool=False, token: str='', firstName: str='', lastName: str='') -> None:
            super().__init__()
            self.Success = success
            self.Token = token
            self.FirstName = firstName
            self.LastName = lastName

class Login:
    class Request(ServerRequestModel):
        def __init__(self, eLabKey: str='', firstName: str='', lastName: str='') -> None:
            super().__init__()
            self.ELabKey = eLabKey
            self.FirstName = firstName
            self.LastName = lastName

    class Response(Model):
        def __init__(self, success: bool=False) -> None:
            super().__init__()
            self.Success = success

class AddSample:
    class Request(ServerRequestModel):
        def __init__(self, file: str='', sampleId: str='', name: str='') -> None:
            super().__init__()
            self.File = file
            self.SampleId = sampleId
            self.Name = name

    class Response(Model):
        def __init__(self, success: bool=False, sampleName: str='', message: str='') -> None:
            super().__init__()
            self.Success = success
            self.SampleName = sampleName
            self.Message = message

class ProviderInfo(Model):
    def __init__(self, name: str='', lastUse: float=0) -> None:
        self.Name = name
        self.LastUse = lastUse
        # self.Description = desc

class ProviderFunction(AbbreviatedEnum):
    LIST = 1
    SEARCH = 2
    CALL = 3

class ProviderRequest(ServerRequestModel):
    def __init__(self, endpont: ProviderFunction, body: dict[str, Primitive]={}) -> None:
        super().__init__()
        self.Endpoint = str(endpont)
        self.Body = body

class ListProviders(TransctionSet):
    class Request(ProviderRequest):
        def __init__(self) -> None:
            super().__init__(ProviderFunction.LIST)

    class Response(Model):
        def __init__(self, providers: list[ProviderInfo]=[]) -> None:
            super().__init__()
            self.Providers = providers
            
        @classmethod
        def Load(cls, serialized: bytes | str | dict, typesDict: type[SerializableTypes]=None):
            if typesDict is None: typesDict = ServerSerializableTypes 
            return super().Load(serialized, typesDict=typesDict)

# class Search:
#     class Request(ServerRequestModel):
#         def __init__(self, sampleId:str='') -> None:
#             super().__init__()
#             self.SampleId = sampleId

#     class Response(Model):
#         def __init__(self, found: bool=False, report:str='') -> None:
#             super().__init__()
#             self.Found = found
#             self.Report = report

class Search(TransctionSet):
    class Request(ProviderRequest):
        def __init__(self, query: str | list[str] = '', providerNames: list[str]=[]) -> None:
            super().__init__(ProviderFunction.SEARCH)
            self.Query = query
            self.Providers = providerNames

    class Hit(Model):
        def __init__(self, type: str='', data: dict[str, Primitive]={}) -> None:
            self.Type = type
            self.Data = data

    class Response(Model):
        def __init__(self, hits: list[Search.Hit]=[]) -> None:
            super().__init__()
            self.Hits = hits

class CallProvider:
    class Request(ProviderRequest):
        def __init__(self, providerName: str, body: Providers.Generic) -> None:
            super().__init__(ProviderFunction.CALL)
            self.Body = body
            self.Provider = providerName

    # response is just a Providers.Generic

class ErrorModel(Model):
    def __init__(self, code: int, message: str) -> None:
        super().__init__()
        self.ErrorCode = code
        self.Message = message

class ServerSerializableTypes(Providers.ProviderSerializableTypes):
    PROVIDER_INFO = ProviderInfo.Load, ProviderInfo()
    SEARCH_HIT = Search.Hit.Load, Search.Hit()
