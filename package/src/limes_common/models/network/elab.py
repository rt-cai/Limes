import json
from requests import Response

from . import _tryParse, ResponseModel


class Login:
    @classmethod
    def MakeRequest(cls, username: str, password: str):
        return {
            'username': username,
            'password': password,
        }

    class Response(ResponseModel):
        def __init__(self, res: Response) -> None:
            super().__init__(res)
            data = json.loads(res.text) if self.Code==200 else {}
            self.Success = self.Code==200
            self.Token = _tryParse(str, data, 'token', '')
            userData = data['user'] if self.Success else {}
            self.FirstName = _tryParse(str, userData, 'firstName', '')
            self.LastName = _tryParse(str, userData, 'lastName', '')