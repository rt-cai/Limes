import requests as Requests
import uuid
from getpass import getuser
import os
from typing import Any, Callable, TypeVar, Union

from limes_common.models.basic import AbbreviatedEnum

from . import Connection
from .. import config
from limes_common.models.network import Model, Primitive, server as Models
from limes_common.models.network.endpoints import ServerEndpoint

class SessionRequest(AbbreviatedEnum):
    GET = 1
    POST = 2

T = TypeVar('T')
class ServerConnection(Connection):
    def __init__(self) -> None:
        super().__init__(config.SERVER_URL)

        self._id = ('%012x:%s:%s' % (uuid.getnode(), getuser(), os.getppid()))
        self._csrf = ''
        try:
            raw = self.session.get(self._makeUrl(ServerEndpoint.INIT))
            res = Models.Init.Response.FromResponse(raw)
            if res._responseCode == 200:
                self._csrf = res.CsrfToken
            self.Ready = True
        except Requests.exceptions.ConnectionError:
            print('*** limes server is not reachable ***')
            self.Ready = False

    def _csrfAuth(self):
        return {config.CSRF_NAME: self._csrf}

    def _compile(self, data: Models.ServerRequestModel) -> dict[str, Any]:
        data.ClientId = self._id
        d = data.ToDict()
        # d[config.CSRF_NAME] = self._csrf
        return d

    # todo this doesn't actually do anythin if just throws an error
    def _notConnectedGuard(self):
        if not self.Ready: raise Requests.exceptions.ConnectionError('limes server not connected')

    def _send(self, url:ServerEndpoint, reqModel: Models.ServerRequestModel, constr: Callable[..., T], req: SessionRequest=SessionRequest.POST) -> T:
        self._notConnectedGuard()
        switcher = {
            SessionRequest.GET: self.session.get,
            SessionRequest.POST: self.session.post
        }
        return constr(switcher[req](
            self._makeUrl(url),
            json=self._compile(reqModel),
            headers = self._csrfAuth()
        ))

    def Authenticate(self) -> Models.Authenticate.Response:
        return self._send(
            ServerEndpoint.AUTHENTICATE,
            Models.Authenticate.Request(self._id),
            Models.Authenticate.Response.FromResponse
        )

    def Login(self, eLabKey: str, firstName: str, lastName: str) -> Models.Login.Response:
        return self._send(
            ServerEndpoint.LOGIN,
            Models.Login.Request(eLabKey, firstName, lastName),
            Models.Login.Response.FromResponse
        )

    def ListProviders(self) -> Models.ListProviders.Response:
        return self._send(
            ServerEndpoint.PROVIDERS,
            Models.ListProviders.Request(),
            Models.ListProviders.Response.FromResponse
        )

    def Search(self, query: Union[str, list[str]], provider_whitelist: list[str]=[]) -> Models.Search.Response:
        return self._send(
            ServerEndpoint.PROVIDERS,
            Models.Search.Request(query, provider_whitelist),
            Models.Search.Response.FromResponse
        )

    def Call(self, provider: str, request: Models.Providers.Generic) -> Models.Providers.Generic:
        return self._send(
            ServerEndpoint.PROVIDERS,
            Models.CallProvider.Request(provider, request),
            Models.Providers.Generic.FromResponse
        )

    # def Add(self, sampleId: str, absPath: str, fileName: str, file: BufferedReader) -> Models.Add.Response:
    #     self._notConnectedGuard()
    #     return Models.Add.Response.FromResponse(self.session.post(
    #         self._makeUrl(ServerEndpoint.ADD),
    #         json=self._compile(Models.Add.Request(sampleId, absPath, fileName)),
    #         headers=self._csrfAuth()
    #         # files={Models.Add.FILE_KEY: file},
    #     ))

    # def Blast(self, query: BufferedReader) -> Models.Blast.Response:
    #     self._notConnectedGuard()
    #     return Models.Blast.Response(self.session.post(
    #         self._makeUrl(ServerEndpoint.BLAST),
    #         data=self._compile(Models.Blast.MakeRequest()),
    #         files={Models.Blast.FILE_KEY: query},
    #     ))