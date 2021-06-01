from common.serializable import Serializable
import json
from json.decoder import JSONDecoder
from typing import Tuple
from models.network import HttpMethod
from common.config import ActiveGeneric as Config

class Requester:
    def __init__(self) -> None:
        self._jsonDecoder = JSONDecoder()

    def SendRequest(self, url: str, endpoint: str, method: HttpMethod, headers: dict = None, body: Serializable = None) -> Tuple[bool, dict]:
        fullurl = '%s%s' % (url, endpoint)
        strBody = body.Serialize()
        res = method.Invoke(fullurl, headers=headers, data=strBody, verify=Config.VERIFY_CERTIFICATE)
        data = self._jsonDecoder.decode(res.text)
        if res.status_code == 200:
            return True, data
        else:
            data['code'] = res.status_code
            return False, data