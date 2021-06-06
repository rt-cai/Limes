import json

from .models.network import HttpMethod
from .requester import SendRequest

_ELAB_URL = 'https://us.elabjournal.com/api/v1/'

def Login(username: str, password: str) -> tuple[bool, str]:
    success, res = SendRequest(_ELAB_URL, 'auth/user', HttpMethod.POST, headers=None, body = {
        'username': username,
        'password': password,
    })

    token = json.loads(res.Raw)
    print(token)