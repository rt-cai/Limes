import requests as Requests
import uuid
from getpass import getuser
import os
from functools import reduce

import limes_common.models.network.server as Server
import limes_common.models.network.elab as ELab
from limes_common.models.network.endpoints import ELabEndpoint, ServerEndpoint, Endpoint
from . import config

class Connection:
    def __init__(self, url) -> None:
        self.session = Requests.session()
        self._URL: str = url

    def _makeUrl(self, ep: Endpoint):
        return (self._URL if self._URL.endswith('/') else self._URL[:-1]) + ep.path

class ServerConnection(Connection):
    def __init__(self) -> None:
        super().__init__(config.SERVER_URL)
        self._id = ('%012x:%s:%s' % (uuid.getnode(), getuser(), os.getppid()))
        # todo, handle server not there
        res = Server.Init.Response(self.session.get(self._makeUrl(ServerEndpoint.INIT)))
        if res.Code == 200:
            self._csrf = res.Csrf
        else:
            raise Exception('failed to reach server')
            
    def Authenticate(self) -> Server.Authenticate.Response:
        SA = Server.Authenticate
        return SA.Response(self.session.post(
            self._makeUrl(ServerEndpoint.AUTHENTICATE),
            data=SA.MakeRequest(self._id, self._csrf)
        ))

    def Login(self, eLabKey: str, firstName: str, lastName: str) -> Server.Login.Response:
        return Server.Login.Response(self.session.post(
            self._makeUrl(ServerEndpoint.LOGIN),
            data=Server.Login.MakeRequest(self._id, eLabKey, firstName, lastName, self._csrf)
            ))

class ELabConnection(Connection):
    def __init__(self) -> None:
        super().__init__(config.ELAB_URL)
        self._token: str = ''

    def SetToken(self, token:str) -> None:
        self._token = token

    def LoggedIn(self) -> bool:
        return self._token != ''

    def Login(self, username: str, password: str) -> ELab.Login.Response:
        return ELab.Login.Response(self.session.post(
            self._makeUrl(ELabEndpoint.LOGIN),
            data=ELab.Login.MakeRequest(username, password)
        ))

    def GetSamples(self, strIds: list[str]) -> ELab.Sample.ListResponse:
        ids = list(int(id[-9:] if len(id) > 9 else id) for id in strIds)
        query = '' if len(strIds)==0 else '?sampleID=' + reduce(lambda s, id: '%s,%s' % (s, id), ids, '')[1:]
        return ELab.Sample.ListResponse(self.session.get(
            '%s/%s%s' % (self._makeUrl(ELabEndpoint.SAMPLES), 'get', query),
            headers={'authorization': self._token}
        ))
