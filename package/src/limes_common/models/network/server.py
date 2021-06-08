import json
from requests import Response

from limes_common import config
from . import _tryParse, ResponseModel

def _tryGetSuccess(data: dict) -> bool:
    try:
        return bool(data.get('success'))
    except:
        return False

class Init:
    @classmethod
    def MakeResponse(cls, csrfToken: str):
        return {config.CSRF_KEY: csrfToken}

    class Response(ResponseModel):
        def __init__(self, res: Response) -> None:
            super().__init__(res)
            if self.Code == 200:
                try:
                    self.Csrf = json.loads(res.text)[config.CSRF_KEY]
                except:
                    self.Csrf = ''

class Authenticate:
    @classmethod
    def MakeRequest(cls, id: str, csrf: str):
        return {
            'id': id,
            config.CSRF_KEY: csrf,
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
        def __init__(self, res: Response) -> None:
            super().__init__(res)
            data = json.loads(res.text) if self.Code==200 else {}
            self.Success = _tryParse(bool, data, 'success', False)
            self.ELabKey = _tryParse(str, data, 'token', '')
            self.FirstName = _tryParse(str, data, 'fName', '')
            self.LastName = _tryParse(str, data, 'lName', '')

class Login:
    @classmethod
    def MakeRequest(cls, id: str, eLabKey: str, firstName: str, lastName: str, csrf: str):
        return {
            config.CSRF_KEY: csrf,
            'fName': firstName,
            'lName': lastName,
            'token': eLabKey,
            'id': id,
            }

    @classmethod
    def MakeResponse(cls, success: bool):
        return {
            'success': success,
            }

    class Request:
        def __init__(self, raw: dict) -> None:
            self.Token = str(raw.get('token'))
            self.Id = str(raw.get('id'))
            self.FirstName = str(raw.get('fName'))
            self.LastName = str(raw.get('lName'))

    class Response(ResponseModel):
        def __init__(self, res: Response) -> None:
            super().__init__(res)
            data = json.loads(res.text) if self.Code==200 else {}
            self.Success = _tryParse(bool, data, 'success', False)

