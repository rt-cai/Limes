import inspect

from . import Model

class Message(Model):
    def __init__(self, mid: str='', body: str='', isError:bool=False) -> None:
        self.MessageID = mid
        self.Body = body
        self.IsError = isError

class Status:
    class Request(Model):
        def __init__(self, msg: str = '') -> None:
            super().__init__()
            self.Msg = msg

    class Response(Model):
        def __init__(self, online: bool=False, echo: str='', msg: str='') -> None:
            super().__init__()
            self.Online = online
            self.Echo = echo
            self.Msg = msg

class Service(Model):
    def __init__(self, requestModelExample: Model, responseModelExample: Model) -> None:
        print(requestModelExample.ToDict())


class Schema:
    class Response(Model):
        def __init__(self, services: list[Service]=[]) -> None:
            self.Services = services