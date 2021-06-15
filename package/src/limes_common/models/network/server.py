from io import BufferedReader
import json
from typing import Any, overload
from requests import Response as py_Response

from limes_common import config
from limes_common.models.basic import AbbreviatedEnum
from . import _tryParse, ResponseModel

class Locations(AbbreviatedEnum):
    ELAB = 1
    SHAMWOW = 2

CLIENT_ID_KEY = 'id'

class Init:
    @classmethod
    def MakeResponse(cls, csrfToken: str):
        return {config.CSRF_KEY: csrfToken}

    class Response(ResponseModel):
        def __init__(self, res: py_Response) -> None:
            super().__init__(res)
            if self.Code == 200:
                try:
                    self.Csrf = json.loads(res.text)[config.CSRF_KEY]
                except:
                    self.Csrf = ''

class Authenticate:
    @classmethod
    def MakeRequest(cls, id: str):
        return {
            CLIENT_ID_KEY: id,
            }

    @classmethod
    def MakeResponse(cls, success: bool, token: str, firstName: str, lastName: str):
        return {
            'fName': firstName,
            'lName': lastName,
            'success': success,
            'token': token,
            }

    class Request:
        def __init__(self, raw: dict) -> None:
            self.Id: str = str(raw.get('id'))

    class Response(ResponseModel):
        def __init__(self, res: py_Response) -> None:
            super().__init__(res)
            data = json.loads(res.text) if self.Code==200 else {}
            self.Success = _tryParse(bool, data, 'success', False)
            self.ELabKey = _tryParse(str, data, 'token', '')
            self.FirstName = _tryParse(str, data, 'fName', '')
            self.LastName = _tryParse(str, data, 'lName', '')

class Login:
    @classmethod
    def MakeRequest(cls, eLabKey: str, firstName: str, lastName: str):
        return {
            'fName': firstName,
            'lName': lastName,
            'token': eLabKey,
            }

    @classmethod
    def MakeResponse(cls, success: bool):
        return {
            'success': success,
            }

    class Request:
        def __init__(self, raw: dict) -> None:
            self.Token = str(raw.get('token'))
            self.Id = str(raw.get(CLIENT_ID_KEY))
            self.FirstName = str(raw.get('fName'))
            self.LastName = str(raw.get('lName'))

    class Response(ResponseModel):
        def __init__(self, res: py_Response) -> None:
            super().__init__(res)
            data = json.loads(res.text) if self.Code==200 else {}
            self.Success = _tryParse(bool, data, 'success', False)


class Add:
    FILE_KEY = 'file'

    @classmethod
    def MakeRequest(cls, sampleId: str, path: str, fileName: str):
        return {
            'path': path,
            'sampleId': sampleId,
            'name': fileName
            }

    @classmethod
    def MakeResponse(cls, success: bool, msg: str=''):
        return {
            'success': success,
            'msg': msg
            }

    class Request:
        def __init__(self, raw: dict) -> None:
            self.ClientId = str(raw.get(CLIENT_ID_KEY))
            self.FilePath = str(raw.get('path'))
            self.SampleId = str(raw.get('sampleId'))
            self.FileName = str(raw.get('name'))

    class Response(ResponseModel):
        def __init__(self, res: py_Response) -> None:
            super().__init__(res)
            data = json.loads(res.text) if self.Code==200 else {}
            self.Success = _tryParse(bool, data, 'success', False)
            self.Message = _tryParse(str, data, 'msg', '')