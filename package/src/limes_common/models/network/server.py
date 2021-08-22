from __future__ import annotations
# from io import BufferedReader
# import json
# from typing import Any, overload
# from requests import Response as py_Response

# from limes_common import config
# from limes_common.connections import eLab
# from limes_common.models.basic import AbbreviatedEnum
# from . import _tryParse, ResponseModel
from . import Model

class Init:
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

class Add:
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

class Search:
    class Request(ServerRequestModel):
        def __init__(self, sampleId:str='') -> None:
            super().__init__()
            self.SampleId = sampleId

    class Response(Model):
        def __init__(self, found: bool=False, report:str='') -> None:
            super().__init__()
            self.Found = found
            self.Report = report

# class FileMeta:
#     def __init__(self, raw:dict = {}) -> None:
#         self.FilePath = str(raw.get('path'))
#         self.SampleId = str(raw.get('sampleId'))
#         self.FileName = str(raw.get('name'))

# class Add:
#     FILE_KEY = 'file'

#     @classmethod
#     def MakeRequest(cls, sampleId: str, path: str, fileName: str):
#         return {
#             'path': path,
#             'sampleId': sampleId,
#             'name': fileName
#             }

#     @classmethod
#     def MakeResponse(cls, success: bool, sampleName: str='', message: str=''):
#         return {
#             'success': success,
#             'msg': message,
#             'sampleName': sampleName,
#             }

#     class Request:
#         def __init__(self, raw: dict) -> None:
#             self.ClientId = str(raw.get(CLIENT_ID_KEY))
#             self.Meta = FileMeta(raw)

#     class Response(ResponseModel):
#         def __init__(self, res: py_Response) -> None:
#             super().__init__(res)
#             data = json.loads(res.text) if self.Code==200 else {}
#             self.Success = _tryParse(bool, data, 'success', False)
#             self.Message = _tryParse(str, data, 'msg', '')
#             self.SampleName = _tryParse(str, data, 'sampleName', '')

# class Search:
#     @classmethod
#     def MakeRequest(cls, sampleId: str):
#         return {
#             'id': sampleId
#         }

#     @classmethod
#     def MakeResponse(cls, success: bool, report: str):
#         return {
#             'success': success,
#             'report': report,
#             }

#     class Request:
#         def __init__(self, raw: dict) -> None:
#             self.ClientId = str(raw.get(CLIENT_ID_KEY))
#             self.Meta = FileMeta(raw)

#     class Response(ResponseModel):
#         def __init__(self, res: py_Response) -> None:
#             super().__init__(res)
#             self.Success = _tryParse(bool, self.data, 'success', False)
#             self.Result = _tryParse(str, self.data, 'report', '')

# class Blast:
#     FILE_KEY = 'query'
#     @classmethod
#     def MakeRequest(cls):
#         return {}

#     @classmethod
#     def MakeResponse(cls, success: bool, report: str):
#         return {
#             'success': success,
#             'report': report,
#             }
#     class Response(ResponseModel):
#         def __init__(self, res: py_Response) -> None:
#             super().__init__(res)
#             self.Success = _tryParse(bool, self.data, 'success', False)
#             self.Result = _tryParse(str, self.data, 'report', '')