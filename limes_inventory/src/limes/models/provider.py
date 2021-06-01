from json.encoder import JSONEncoder
from typing import Callable

from common.config import ActiveProvider as Config
from common.serializable import Serializable
from coms.server import Server
from coms.requester import Requester
from models.network import *
from models.basic import AbbreviatedEnum

# class Responsibility(AbbreviatedEnum):
#     FASTA = 1

class RegistrationForm(Serializable):
    def __init__(self, string: str) -> None:
        self.Address = None
        # self.Responsibilities = None
        super().__init__(string)

    def _deserialize(self, string: str) -> None:
        vals = self._formatObject(string)
        for k in self.__dict__.keys():
            self.__setattr__(k, vals[k])

    def Serialize(self) -> str:
        # return '{"Address": "%s","Responsibilities": "%s"}'
        return str(self.__dict__).replace("'", '"')

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
        class MyRegistrationForm(RegistrationForm):
            def __init__(self) -> None:
                self.Address = fulladdress
        form = MyRegistrationForm()
        success, response = r.SendRequest(Config.CORE_ADDRESS, Endpoints.REGISTER, HttpMethod.POST, body = form)

        if success:
            self._server.Serve()
        else:
            print(response)