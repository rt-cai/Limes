from typing import Callable, TypeVar
from requests import Response
import json


T = TypeVar('T')
U = TypeVar('U')
def _tryParse(constr: Callable[[T], U], data: dict[str, T], key: str, default: U) -> U:
    val = data.get(key)
    if val:
        return constr(val)
    else:
        return default

class ResponseModel:
    def __init__(self, res: Response) -> None:
        self.Code = res.status_code
        self.data: dict = json.loads(res.text) if self.Code==200 else {}