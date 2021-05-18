import json
from json.decoder import JSONDecoder
from json.encoder import JSONEncoder
from typing import Tuple
from models.network import HttpMethod
from common.config import ActiveGeneric as Config

class Requester:
    def __init__(self) -> None:
        self._jsonDecoder = JSONDecoder()
        self._jsonEncoder = JSONEncoder()

    def SendRequest(self, url: str, endpoint: str, method: HttpMethod, headers: dict = None, body: dict = None) -> Tuple[bool, dict]:
        fullurl = '%s%s' % (url, endpoint)
        strBody = self._jsonEncoder.encode(body)
        res = method.Invoke(fullurl, headers=headers, data=strBody, verify=Config.VERIFY_CERTIFICATE)
        data = self._jsonDecoder.decode(res.text)
        if res.status_code == 200:
            return True, data
        else:
            data['code'] = res.status_code
            return False, data