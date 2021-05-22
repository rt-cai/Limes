from enum import Enum
import json
from common.config import ActiveGeneric as Config
from json.decoder import JSONDecoder
from typing import Callable, Tuple
from models.inventory import Sample
from models.provider import RegistrationForm as _providerRegistration
from models.basic import PublicOnlyDict, AdvancedEnum
import requests as py_requests

class HttpMethod(AdvancedEnum):
    GET = 1, py_requests.get
    POST = 2, py_requests.post
    PUT = 3, py_requests.put

    def __init__(self, _: int, function: Callable[..., py_requests.Response]) -> None:
        self.Invoke = function

class Endpoints(AdvancedEnum):
    REGISTER = 1, _providerRegistration

    def __init__(self, _: int, data: PublicOnlyDict) -> None:
        self.DataModel = data

    def __str__(self) -> str:
        default = super().__str__()
        start = default.find(self.name)
        return default[start:].lower()

# request types
class ResponseType(Enum):
    HTML = 1
    JSON = 2

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
            return False, None

# response types
class Response:
    def __init__(self, code: int, type: ResponseType, body) -> None:
        self.Type = type
        self.Code = code
        self.Body = body

    def Serialize(self):
        raise NotImplementedError

class ErrorResponse(Response):
    def __init__(self, code: str, type: ResponseType, body):
        assert code != 200
        super().__init__(code, type, body)


class ServerErrorResponse(ErrorResponse):
    def __init__(self, message: str):
        body = {
            'message': message
        }
        super().__init__(500, ResponseType.JSON, body)

    def Serialize(self):
        return json.dumps(self.Body)

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
        return json.dumps(self.Body)

class SampleResponse(JsonResponse):
    def __init__(self, sample: Sample) -> None:
        super().__init__(sample.__dict__)
    