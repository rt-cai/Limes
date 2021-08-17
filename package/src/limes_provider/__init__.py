from limes_common.models.network import provider as Models
from limes_common.exceptions import AbstractClassException

_notImplimentedMsg = 'Call on abstract provider. Funciton not implimented.'

class ProviderConnection:
    def __init__(self, name:str) -> None:
        self.Name = name

    def CheckStatus(self, msg: str='') -> Models.Status.Response:
        raise AbstractClassException(_notImplimentedMsg)
