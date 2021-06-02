from requests.api import head
from ..models.serializable import Serializable
from ..config import ActiveGeneric as Config
from json.decoder import JSONDecoder
from typing import Tuple, Union
from ..models.network import HttpMethod

class Requester:
    def __init__(self) -> None:
        self._jsonDecoder = JSONDecoder()

    def SendRequest(self, url: str, endpoint: str, method: HttpMethod, headers: dict = None, body = None) -> Tuple[bool, dict]:
        fullurl = '%s%s' % (url, endpoint)
        # strBody = str(body)
        res = method.Invoke(fullurl, headers=headers, data=body, verify=Config.VERIFY_CERTIFICATE)
        # print(res.status_code)
        # print(res.text)
        if res.status_code == 200:
            data = self._jsonDecoder.decode(res.text)
            return True, data
        else:
            data = {'code': res.status_code}
            return False, data