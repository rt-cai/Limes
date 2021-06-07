class IServer:
    def Login(self, username: str, password: str) -> bool:
        raise NotImplementedError

class LoginResponse:
    def __init__(self) -> None:
        pass