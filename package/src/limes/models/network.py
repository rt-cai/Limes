from enum import Enum
import json
from ..config import ActiveGeneric as Config
from json.decoder import JSONDecoder
from typing import Callable, Tuple
from .inventory import Sample
from .basic import AbbreviatedEnum, AdvancedEnum
import requests as py_requests

class HttpMethod(AdvancedEnum, AbbreviatedEnum):
    GET = 1, py_requests.get
    POST = 2, py_requests.post
    PUT = 3, py_requests.put

    def __init__(self, _: int, function: Callable[..., py_requests.Response]) -> None:
        self.Invoke = function



# request types
class ContentType(AbbreviatedEnum):
    HTML = 1
    JSON = 2
    CSS = 3
    JAVASCRIPT = 4

    PNG = 5
    def __str__(self) -> str:
        prefix = 'text'
        if self.value == 5:
            prefix = 'image'
        return ('%s/%s' % (prefix, super().__str__())).lower()

class Request:
    def __init__(self, headers: dict, path: str, body:bytes=None):
        self.Headers = headers
        self.Path = path
        self.body = body

    def TryGetJsonBody(self, jsonDecoder: JSONDecoder) -> Tuple[bool, dict]:
        strBody = self.body.decode(Config.ENCODING)
        try:
            return True, jsonDecoder.decode(strBody)
        except:
            return False, {}

# response types
class Response:
    def __init__(self, code: int, type: ContentType, body) -> None:
        self.Type = type
        self.Code = code
        self.Body = body
        self.Bytes = None

    def Serialize(self) -> str:
        return str(self.Body)

class ErrorResponse(Response):
    def __init__(self, code: int, type: ContentType, body: str):
        assert code != 200
        super().__init__(code, type, body)

class ServerErrorResponse(ErrorResponse):
    def __init__(self, message: str):
        body = {
            'message': message
        }
        super().__init__(500, ContentType.JSON, str(body))

    def Serialize(self):
        return json.dumps(self.Body)

class SuccessResponse(Response):
    def __init__(self, type: ContentType, body):
        super().__init__(200, type, body)

class HtmlResponse(SuccessResponse):
    def __init__(self, body: str) -> None:
        super().__init__(ContentType.HTML, body)

    def Serialize(self):
        return self.Body

class JsonResponse(SuccessResponse):
    def __init__(self, body: dict) -> None:
        super().__init__(ContentType.JSON, body)

    def Serialize(self):
        return json.dumps(self.Body)

class SampleResponse(JsonResponse):
    def __init__(self, sample: Sample) -> None:
        super().__init__(sample.__dict__)
    