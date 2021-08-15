class ProviderResponseItem:
    pass

class Result:
    def __init__(self, success: bool, msg: str = '', result: list[ProviderResponseItem] = []) -> None:
        self.Success = success
        self.Msg = msg
        self.Result = result