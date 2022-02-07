from typing import Any, Union
import os

from .connections import eLab
from .models import Primitive, Model, provider as ProviderModels
from .models.elab import Sample

class Limes:
    pass
    # def __init__(self) -> None:
    #     self._server = server.ServerConnection()
    #     self._eLab = eLab.ELabConnection()

    #     self.CallProvider = self._server.CallProvider
    #     self.GetSample = self._eLab.GetSample
    #     self.GetStorage = self._eLab.GetStorage
    #     self.GetFullStoragePath = self._eLab.GetFullStoragePath
    #     self.ReloadStorages = self._eLab.ReloadStorages

    # #   def _auth() -> tuple[bool, str]:
    # def _auth(self) -> bool:
    #     res = self._server.Authenticate()
    #     if res.Code != 200:
    #         return False

    #     if res.Success:
    #         print('Authenticated terminal as %s' % res.FirstName)
    #         # return True, res.FirstName
    #         self._eLab.SetAuth(res.Token)
    #     else:
    #         # return False, ''
    #         print('Not logged in')
    #     return res.Success

    # def Login(self, username, password) -> tuple[bool, str]:
    #     if not self._server.Ready and not self._server.Reconnect(): 
    #         return False, 'unable to connect to server'
    #     res = self._server.Login(username, password)

    #     if res.Code == 200:
    #         self._eLab.SetAuth(res.ElabToken)
    #         return True, 'logged in as %s' % res.FirstName
    #     elif res.Code == 401:
    #         return False, 'incorrect credentials'
    #     else:
    #         return False, 'failed with code [%s], msg [%s]' % (res.Code, res.Error)

    # def Login_from_file(self, path: str) -> tuple[bool, str]:
    #     try:
    #         with open(path) as credFile:
    #             cred = credFile.readlines()
    #             u = cred[0]
    #             p = cred[1]
    #             return self.Login(u, p)
    #     except Exception as e:
    #         return False, str(e)

    # def ListProviders(self):
    #     res = self._server.List()
    #     es = self._eLab.GetSchema()
    #     ei = ServerModels.ProviderInfo()
    #     ei.Name = 'eLab'
    #     ei.Schema = es
    #     if res.Providers is None:
    #         res.Providers = [ei]
    #     else:
    #         res.Providers.append(ei)
    #     return res

    # def Search(self, query: str):
    #     s_res = self._server.Search(query)
    #     e_res = self._eLab.Search(query)
    #     return s_res.AddFrom(e_res)