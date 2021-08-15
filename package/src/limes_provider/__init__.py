from limes_common.models.provider import Result

_notImplimentedResult = Result(False, msg='Call on abstract provider. Funciton not implimented.')

class ProviderConnection:
    def __init__(self, name:str) -> None:
        self.Name = name

    def CheckStatus(self) -> Result:
        return _notImplimentedResult

    def DataBySample(self, sampleId: str) -> Result:
        return _notImplimentedResult
