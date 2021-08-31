import requests as Requests
import uuid
from getpass import getuser
import os
from typing import Any, Callable, TypeVar, Union

from ..http import HttpConnection
from ... import config
from ...models import Model, Primitive, server as Models, provider
from ...models.endpoints import ServerEndpoint

T = TypeVar('T')
class ServerConnection(HttpConnection):
    def __init__(self) -> None:
        super().__init__(config.SERVER_URL)

        self._id = ('%012x:%s:%s' % (uuid.getnode(), getuser(), os.getppid()))
        self._csrf = ''
        try:
            raw = self.session.get(self._makeUrl(ServerEndpoint.INIT.Path))
            res = Models.Init.Response.Parse(raw)
            if res._responseCode == 200:
                self._csrf = res.CsrfToken
            self.Ready = True
        except Requests.exceptions.ConnectionError:
            print('*** limes server is not reachable ***')
            self.Ready = False

    def _makeHeader(self):
        return {config.CSRF_NAME: self._csrf}

    def _makeJson(self, data: Models.ServerRequest) -> dict[str, Any]:
        data.ClientId = self._id
        d = data.ToDict()
        # d[config.CSRF_NAME] = self._csrf
        return d

    def Authenticate(self):
        req = Models.ServerRequest()
        return self.MakeRequest(req)
        return self.Send(
            Models.Authenticate.Request(self._id),
            Models.Authenticate.Response.Parse
        )

    # def CheckStatus(self, msg: str='') -> provider.Status.Response:
    #     res = self.Authenticate()
    #     if not isinstance(res, ErrorModel):
    #         return provider.Status.Response(res.Success, msg='%s %s' % (res.FirstName, res.LastName))
    #     return provider.Status.Response(False)

    # def GetSchema(self) -> provider.Schema:
    #     raise AbstractClassException(_notImplimentedMsg)

    # def MakeRequest(self, purpose: str, request: Primitive) -> Primitive:
    #     raise AbstractClassException(_notImplimentedMsg)
