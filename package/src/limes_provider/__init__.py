from typing import Any

from limes_common.models.network import provider as Models
from limes_common.exceptions import AbstractClassException

_notImplimentedMsg = 'Call on abstract provider. Funciton not implimented.'

class ProviderConnection:
    def CheckStatus(self, msg: str='') -> Models.Status.Response:
        raise AbstractClassException(_notImplimentedMsg)

    def GetSchema(self) -> Models.Schema:
        raise AbstractClassException(_notImplimentedMsg)

    def MakeRequest(self, request: dict[str, Any]) -> dict[str, Any]:
        raise AbstractClassException(_notImplimentedMsg)


