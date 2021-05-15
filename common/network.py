from enum import Enum
from typing import Callable
from common.models import Sample
import requests as py_requests

class HttpMethod(Enum):
    GET = 1, py_requests.get
    POST = 2, py_requests.post
    PUT = 3, py_requests.put

    def __new__(cls, *args, **kwds):
        obj = object.__new__(cls)
        obj._value_ = args[0]
        return obj

    def __init__(self, _: int, function: Callable[..., py_requests.Response]) -> None:
        self.Send = function

# request types
class ResponseType(Enum):
    HTML = 1
    JSON = 2

class Request:
    def __init__(self, headers: dict, path: str):
        self.Headers = headers
        self.Path = path
    pass

# response types
class Response:
    def __init__(self, code: int, type: ResponseType, body) -> None:
        self.Type = type
        self.Code = code
        self.Body = body

    def Serialize(self):
        raise NotImplementedError

class ErrorResponse(Response):
    def __init__(self, code: str, type: ResponseType, body: str):
        assert code != 200
        super().__init__(code, type, body)

    def Serialize(self):
        return self.Body

class SuccessResponse(Response):
    def __init__(self, type: ResponseType, body):
        super().__init__(200, type, body)

class HtmlResponse(SuccessResponse):
    def __init__(self, body: str) -> None:
        super().__init__(ResponseType.HTML, body)

    def Serialize(self):
        return self.Body

class JsonResponse(SuccessResponse):
    def __init__(self, body: dict) -> None:
        super().__init__(ResponseType.JSON, body)

    def Serialize(self):
        return str(self.Body)

class SampleResponse(JsonResponse):
    def __init__(self, sample: Sample) -> None:
        super().__init__(sample.__dict__)
    