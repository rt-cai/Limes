from enum import Enum
import requests as py_requests
from json import JSONDecoder

from common import Sample, SampleResponse
from config import Active as Config

class SearchMethod(Enum):
    NAME = 1

class _Query:
    def __init__(self, type: SearchMethod):
        self.Type = type

    # abstract
    def Stringify(self):
        raise NotImplementedError

    def _getBaseJson(self) -> dict:
        return {
            'Type': self.Type
            }

class NameQuery(_Query):
    def __init__(self, name) -> None:
        super().__init__(SearchMethod.NAME)
        self.Name = name

    def Stringify(self):
        json = self._getBaseJson()
        json['Name'] = self.Name
        return str(json)

class Requester:
    _Core_Address = Config.GetCoreAddress()
    _VERIFY = Config.CLIENT_VERIFY_CERTIFICATE

    def __init__(self) -> None:
        self._apiToken = ''
        pass

    def _getPath(endpoint: str):
        return '%s/%s' % (Requester._Core_Address, endpoint)

    def _send(self, url: str, method: SearchMethod, body: str):
        pass

    def Login(self, username: str, password: str) -> None:
        pass

    def GetSample(self, sampleID: str) -> Sample:
        pass

    def Search(self, method: SearchMethod, query: _Query) -> list[Sample]:
        pass

    def Get(self):
        path = Requester._getPath('test')
        res = py_requests.get(path, verify=self._VERIFY)
        jd = JSONDecoder()
        js = jd.decode(res.text.replace('\'', '"'))   
        print('--')
        print(str(res.content))
        print('--')
        print(res.text)
        print('--')
        print(js)
        print('--')