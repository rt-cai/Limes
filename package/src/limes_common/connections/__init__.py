from typing import Any, TypeVar, Union, Callable
from limes_common.models.basic import AbbreviatedEnum

from limes_common.models import Primitive, Model, provider as Models
from limes_common.exceptions import AbstractClassException
from limes_common.utils import current_time

_notImplimentedMsg = 'Call on abstract provider. Funciton not implimented.'

T = TypeVar('T')
class Connection:
    def __init__(self) -> None:
        self.LastUse = current_time()

    # def CheckStatus(self, echo: str='') -> Models.Status.Response:
    #     raise AbstractClassException(_notImplimentedMsg)

    def GetSchema(self) -> Models.Schema:
        raise AbstractClassException(_notImplimentedMsg)

    def MakeRequest(self, request: Models.ProviderRequest) -> Models.ProviderResponse:
        raise AbstractClassException(_notImplimentedMsg)

    # def Search(self, token: Union[str, list[str]], criteria: list[Criteria]):
    #     raise AbstractClassException(_notImplimentedMsg)
