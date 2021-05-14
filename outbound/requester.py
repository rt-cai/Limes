from common.network import HttpMethod
from enum import Enum
import requests as py_requests
from json import JSONDecoder

from common.config import ActiveGeneric as Config

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
    def __init__(self) -> None:
        self._VERIFY = Config.VERIFY_CERTIFICATE
        pass

    def MakeRequest(self, url: str, endpoint: str, method: HttpMethod, body: dict) -> py_requests.Response:
        fullUrl = url + endpoint

        # print(fullUrl)
        # raise Exception
        return method.PyRequestFunction(url=fullUrl, verify=Config.VERIFY_CERTIFICATE, data=body)

    # def Test(self):
    #     path = self._getPath('test')
    #     res = py_requests.get(path, verify=self._VERIFY)
    #     jd = JSONDecoder()
    #     js = jd.decode(res.text.replace('\'', '"'))   
    #     print('--')
    #     print(str(res.content))
    #     print('--')
    #     print(res.text)
    #     print('--')
    #     print(js)
    #     print('--')