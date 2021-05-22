from json.encoder import JSONEncoder
from typing import Callable

from coms.server import Server
from coms.requester import Requester
from models.network import *
from models.provider import RegistrationForm_Explicit, Responsibility
from common.config import ActiveProvider as Config

class Provider:
    def __init__(self) -> None:
        self._server = Server(Config.URL, Config.PORT)
        self._jsonEncoder = JSONEncoder()

    def AddEndpoint(self, path: str, method: HttpMethod, callback: Callable[[Request], Response]):
        self._server._Add(path, method, callback)

    def Start(self):
        url = Config.URL
        port = Config.PORT
        fulladdress = '%s:%s' % (url, port)
        r = Requester()
        form = RegistrationForm_Explicit(fulladdress, [Responsibility.FASTA])
        success, response = r.SendRequest(Config.CORE_ADDRESS, Endpoints.REGISTER, HttpMethod.POST, body = form.GetDict())

        if success:
            self._server.Serve()
        else:
            print(response)
