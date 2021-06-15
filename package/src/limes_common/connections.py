from io import BufferedReader
import requests as Requests
import uuid
from getpass import getuser
import os
from functools import reduce
import paramiko
from typing import Any

from limes_common.models.network import server, elab
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
        try:
            res = server.Init.Response(self.session.get(self._makeUrl(ServerEndpoint.INIT)))
            if res.Code == 200:
                self._csrf = res.Csrf
            self.Ready = True
        except Requests.exceptions.ConnectionError:
            print('*** limes server is not reachable ***')
            self.Ready = False
    
    def _compile(self, data: dict[str, Any]) -> dict[str, Any]:
        data[config.CSRF_KEY] = self._csrf
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

class ELabConnection(Connection):
    def __init__(self) -> None:
        super().__init__(config.ELAB_URL)
        self._token: str = ''

    def _getAuthHeader(self):
        return {'authorization': self._token}

    def SetToken(self, token:str) -> None:
        self._token = token

    def LoggedIn(self) -> bool:
        return self._token != ''

    def Login(self, username: str, password: str) -> elab.Login.Response:
        return elab.Login.Response(self.session.post(
            self._makeUrl(ELabEndpoint.LOGIN),
            data=elab.Login.MakeRequest(username, password)
        ))

    def _truncateToId(self, id: str) -> int:
        return int(id[-9:] if len(id) > 9 else id)

    def SearchSamplesById(self, strIds: list[str]) -> elab.Sample.ListResponse:
        ids = list(self._truncateToId(id) for id in strIds)
        query = '' if len(strIds)==0 else '?sampleID=' + reduce(lambda s, id: '%s,%s' % (s, id), ids, '')[1:]
        return elab.Sample.ListResponse(self.session.get(
            '%s/%s%s' % (self._makeUrl(ELabEndpoint.SAMPLES), 'get', query),
            headers=self._getAuthHeader()
        ))

    def GetSample(self, strId: str) -> elab.Sample.Response:
        id = self._truncateToId(strId)
        return elab.Sample.Response(self.session.get(
            '%s/%s' % (self._makeUrl(ELabEndpoint.SAMPLES), id),
            headers=self._getAuthHeader()
        ))

class ShamwowConnection():
    def __init__(self) -> None:
        self._URL = config.SHAMWOW_URL
        ssh = paramiko.SSHClient()
        ssh.load_system_host_keys()
        login = {
            "username": "tliu",
            "hostname": self._URL
        }
        
        command = 'ls -lh'

        ssh.connect(**login)
        ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command(command)
        # print(ssh_stdin)
        print(''.join(ssh_stdout.readlines()))
        ssh.close()