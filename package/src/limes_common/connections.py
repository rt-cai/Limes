from enum import Enum
from typing import Callable, ClassVar, overload
import requests as Requests
import uuid
from getpass import getuser
import os

from limes_common.models.basic import AdvancedEnum, AbbreviatedEnum

from .models.network import IServer

class HttpMethod(AdvancedEnum, AbbreviatedEnum):
    GET = 1, Requests.get
    POST = 2, Requests.post
    PUT = 3, Requests.put
    def __init__(self, _: int, function: Callable[..., Requests.Response]) -> None:
        self.Invoke = function

class Connection:
    @classmethod
    def _req(cls, method: HttpMethod, endpoint: str, headers=None, body=None) -> tuple[int, str]:
        res = method.Invoke('%s%s' % (cls._getUrl(), endpoint), headers=headers, data=body)
        return res.status_code, res.text

    @classmethod
    def _getUrl(cls) -> str:
        raise NotImplementedError

class ServerConnection(Connection):
    def __init__(self) -> None:
        self.id = '%s-%s-%012x' % (os.ctermid(), getuser(), uuid.getnode())

    def Login(self, username: str, password: str) -> bool:
        code, raw = ServerConnection._req(HttpMethod.POST, 'login', body={
            'username':username,
            'password': password,
            'id': self.id
        })
        if code ==200:
            print(raw)
        else:
            print(code)
        return code==200

    @classmethod
    def _getUrl(cls):
        return 'https://127.0.0.1:8000/api/d1/'

class ELabConnection(Connection):
    def __init__(self) -> None:
        pass

    def SetToken(self, token:str) -> None:
        pass

    def Login(self, username: str, password: str) -> tuple[bool, str]:
        code, raw = ELabConnection._req(HttpMethod.POST, 'user/auth', body = {
            'username': username,
            'password': password,
        })
        print(code)
        print(raw)
        return code==200, ''

    @classmethod
    def _getUrl(cls):
        return 'https://us.elabjournal.com/api/v1/'