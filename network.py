from enum import Enum

class Method(Enum):
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

class _Response:
    def __init__(self, code: int, type: ResponseType, body) -> None:
        self.Type = type
        self.Code = code
        self.Body = body

class HtmlResponse(_Response):
    def __init__(self, body: str):
        super().__init__(200, ResponseType.HTML, body)

class JsonResponse(_Response):
    def __init__(self, body: dict):
        super().__init__(200, ResponseType.JSON, body)

class ErrorResponse(_Response):
    def __init__(self, code: str, body: str):
        assert code != 200
        super().__init__(code, ResponseType.HTML, body)