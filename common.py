from enum import Enum
from utils import SerializableTime

############################################################
# Sample
############################################################

class Sample:
    def __init__(self) -> None:
        self.Name = ''
        self.ParentId = ''
        self.Location = ''
        self.DateCreated = SerializableTime.now()

############################################################
# Responses
############################################################

class HttpMethod(Enum):
    GET = 1
    POST = 2
    PUT = 3

class ResponseType(Enum):
    HTML = 1
    JSON = 2

class Request:
    def __init__(self, headers: dict, path: str):
        self.Headers = headers
        self.Path = path
    pass

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
    