from . import Model

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