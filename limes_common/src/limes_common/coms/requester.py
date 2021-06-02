from requests.api import head
from limes_common.models.serializable import Serializable
from limes_common.config import ActiveGeneric as Config
import json
from json.decoder import JSONDecoder
from typing import Tuple, Union
from limes_common.models.network import HttpMethod

class Requester:
    def __init__(self) -> None:
        self._jsonDecoder = JSONDecoder()

    def SendRequest(self, url: str, endpoint: str, method: HttpMethod, headers: dict = None, body = None) -> Tuple[bool, dict]:
        fullurl = '%s%s' % (url, endpoint)
        # strBody = str(body)
        res = method.Invoke(fullurl, headers=headers, data=body, verify=Config.VERIFY_CERTIFICATE)
        # print(res.status_code)
        # print(res.text)
        data = self._jsonDecoder.decode(res.text)
        if res.status_code == 200:
            return True, data
        else:
            data['code'] = res.status_code
            return False, data