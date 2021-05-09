from enum import Enum
from typing import Callable

class Method(Enum):
    GET = 'GET'
    POST = 'POST'
    PUT = 'PUT'

class Response:
    pass

class Endpoint:
    def __init__(self, name: str, method: Method, handler: Callable[[], Response]):
        self.NAME = name
        self.METHOD = method
        self._handle = handler

    def Hit(self) -> Response:
        return self._handle()
