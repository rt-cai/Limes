from django.middleware import csrf
import requests as Requests
import uuid
from getpass import getuser
import os
from typing import Any, Text
from io import BufferedReader

from . import Connection
from .. import config
from limes_common.models.network import server
from limes_common.models.network.endpoints import ServerEndpoint

class ServerConnection(Connection):
    def __init__(self) -> None:
        super().__init__(config.SERVER_URL)
        self._id = ('%012x:%s:%s' % (uuid.getnode(), getuser(), os.getppid()))
        self._csrf = ''
        try:
            raw = self.session.get(self._makeUrl(ServerEndpoint.INIT))
            res = server.Init.Response.FromResponse(raw)
            if res.Code == 200:
                self._csrf = res.CsrfToken
            self.Ready = True
        except Requests.exceptions.ConnectionError:
            print('*** limes server is not reachable ***')
            self.Ready = False

    def _csrfAuth(self):
        return {config.CSRF_NAME: self._csrf}

    def _compile(self, data: server.ServerRequestModel) -> dict[str, Any]:
        data.ClientId = self._id
        d = data.ToDict()
        # d[config.CSRF_NAME] = self._csrf
        return d

    # todo this doesn't actually do anythin if just throws an error
    def _notConnectedGuard(self):
        if not self.Ready: raise Requests.exceptions.ConnectionError('limes server not connected')

    def Authenticate(self) -> server.Authenticate.Response:
        self._notConnectedGuard()
        return server.Authenticate.Response.FromResponse(self.session.post(
            self._makeUrl(ServerEndpoint.AUTHENTICATE),
            json=self._compile(server.Authenticate.Request(self._id)),
            headers=self._csrfAuth()
    ))

    def Login(self, eLabKey: str, firstName: str, lastName: str) -> server.Login.Response:
        self._notConnectedGuard()
        return server.Login.Response.FromResponse(self.session.post(
            self._makeUrl(ServerEndpoint.LOGIN),
            json=self._compile(server.Login.Request(eLabKey, firstName, lastName)),
            headers=self._csrfAuth()
        ))

    def Add(self, sampleId: str, absPath: str, fileName: str, file: BufferedReader) -> server.Add.Response:
        self._notConnectedGuard()
        return server.Add.Response.FromResponse(self.session.post(
            self._makeUrl(ServerEndpoint.ADD),
            json=self._compile(server.Add.Request(sampleId, absPath, fileName)),
            headers=self._csrfAuth()
            # files={server.Add.FILE_KEY: file},
        ))

    # def Blast(self, query: BufferedReader) -> server.Blast.Response:
    #     self._notConnectedGuard()
    #     return server.Blast.Response(self.session.post(
    #         self._makeUrl(ServerEndpoint.BLAST),
    #         data=self._compile(server.Blast.MakeRequest()),
    #         files={server.Blast.FILE_KEY: query},
    #     ))