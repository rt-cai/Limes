from typing import Any, TypeVar, Union, Callable
from ..models.basic import AbbreviatedEnum

from ..models import Primitive, Model, provider as Models
from ..exceptions import AbstractMethodException
from ..utils import current_time

_notImplimentedMsg = 'Call on abstract provider. Funciton not implimented.'

T = TypeVar('T')
class Connection:
    # def CheckStatus(self, echo: str='') -> Models.Status.Response:
    #     raise AbstractClassException(_notImplimentedMsg)

    def __init__(self) -> None:
        self._token = ''

    def SetAuth(self, token: str):
        self._token = token

    def Logout(self):
        self._token = ''
        
    def GetSchema(self) -> Models.Schema:
        raise AbstractMethodException(_notImplimentedMsg)

    def MakeRequest(self, request: Models.ProviderRequest) -> Models.ProviderResponse:
        raise AbstractMethodException(_notImplimentedMsg)

    def Search(self, query: str) -> Models.Search.Response:
        raise AbstractMethodException(_notImplimentedMsg)

    def Close(self):
        pass
