from types import Tuple

from ..config import ActiveGeneric as Config
# from json.decoder import JSONDecoder
from .models.network import HttpMethod

class Response:
    def __init__(self, code: int, raw: str) -> None:
        self.Code: int = code
        self.Raw: str = raw

def SendRequest(url: str, endpoint: str, method: HttpMethod, headers: dict = None, body = None) -> tuple[bool, Response]:
    fullurl = '%s%s' % (url, endpoint)
    # strBody = str(body)
    res = method.Invoke(fullurl, headers=headers, data=body, verify=Config.VERIFY_CERTIFICATE)
    # print(res.status_code)
    # print(res.text)
    # if res.status_code == 200:
    #     data = self._jsonDecoder.decode(res.text)
    #     return True, data
    # else:
    #     data = {'code': res.status_code}
    #     # return False, data
    return res.status_code == 200, Response(res.status_code, res.text)