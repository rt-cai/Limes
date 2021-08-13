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
            self.Success = self.Code==200
            self.Token = _tryParse(str, self.data, 'token', '')
            userData = self.data['user'] if self.Success else {}
            self.FirstName = _tryParse(str, userData, 'firstName', '')
            self.LastName = _tryParse(str, userData, 'lastName', '')

class Sample:
    def __init__(self, data: dict = {}) -> None:
        self.Name = _tryParse(str, data, 'name', 'None')
        self.Owner =_tryParse(str, data, 'owner', '')
        self.TimeCreated =_tryParse(str, data, 'created', '')
        self.Id =_tryParse(int, data, 'sampleID', 0)
        self.Barcode =_tryParse(str, data, 'barcode', '')
        self.Description =_tryParse(str, data, 'description', '')
        self.ParentId =_tryParse(int, data, 'parent', 0)

    class ListResponse(ResponseModel):
        def __init__(self, res: Response) -> None:
            super().__init__(res)
            self.samples = list(map(lambda raw: Sample(raw), self.data))