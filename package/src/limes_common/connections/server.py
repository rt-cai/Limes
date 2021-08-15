import requests as Requests
import uuid
from getpass import getuser
import os
from typing import Any
from io import BufferedReader

from . import Connection
from .. import config
from limes_common.models.network import server
from limes_common.models.network.endpoints import ServerEndpoint

class ServerConnection(Connection):
    def __init__(self) -> None:
        super().__init__(config.SERVER_URL)
        self._id = ('%012x:%s:%s' % (uuid.getnode(), getuser(), os.getppid()))
        try:
            res = server.Init.Response(self.session.get(self._makeUrl(ServerEndpoint.INIT)))
            if res.Code == 200:
                self._csrf = res.Csrf
            self.Ready = True
        except Requests.exceptions.ConnectionError:
            print('*** limes server is not reachable ***')
            self.Ready = False

    def _compile(self, data: dict[str, Any]) -> dict[str, Any]:
        data[config.CSRF_NAME] = self._csrf
        data[server.CLIENT_ID_KEY] = self._id
        return data

    def _notConnectedGuard(self):
        if not self.Ready: raise Requests.exceptions.ConnectionError('limes server not connected')

    def Authenticate(self) -> server.Authenticate.Response:
        self._notConnectedGuard()
        return server.Authenticate.Response(self.session.post(
            self._makeUrl(ServerEndpoint.AUTHENTICATE),
        data=self._compile(server.Authenticate.MakeRequest(self._id))
    ))

    def Login(self, eLabKey: str, firstName: str, lastName: str) -> server.Login.Response:
        self._notConnectedGuard()
        return server.Login.Response(self.session.post(
            self._makeUrl(ServerEndpoint.LOGIN),
            data=self._compile(server.Login.MakeRequest(eLabKey, firstName, lastName))
        ))

    def Add(self, sampleId: str, absPath: str, fileName: str, file: BufferedReader) -> server.Add.Response:
        self._notConnectedGuard()
        return server.Add.Response(self.session.post(
            self._makeUrl(ServerEndpoint.ADD),
            data=self._compile(server.Add.MakeRequest(sampleId, absPath, fileName)),
            files={server.Add.FILE_KEY: file},
        ))

    def Blast(self, query: BufferedReader) -> server.Blast.Response:
        self._notConnectedGuard()
        return server.Blast.Response(self.session.post(
            self._makeUrl(ServerEndpoint.BLAST),
            data=self._compile(server.Blast.MakeRequest()),
            files={server.Blast.FILE_KEY: query},
        ))