
from typing import Callable
from .requester import SendRequest
from .models.network import HttpMethod

LoginCallback = Callable[[str, str], tuple[bool, str]]
_onLogin: LoginCallback = lambda u, p: False, ''

def Login(username: str, password: str):
    return _onLogin(username, password)

def SubscribeLogin(callback: LoginCallback):
    