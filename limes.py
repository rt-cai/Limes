from models.inventory import Sample
from json.decoder import JSONDecoder
from typing import Tuple
from requests.api import head

from requests.models import parse_header_links
from common.config import ActiveClient as Config
from models.network import HttpMethod
from requests import Request as py_Requester


class Query():
    def ByAll(searchString: str) -> Tuple[bool, list[Sample]]:
        ENDPOINT = 'samples'
        endpointWithParam = '%s?search=%s' % (ENDPOINT, searchString)
        succeed, response = _sendAuthenticatedRequest(
            Config.ELAB_URL, endpointWithParam, HttpMethod.GET)
        if succeed:
            count = response['recordCount']
            total = response['totalRecords']
            if total > count:
                print('too many hits (%s total), truncated to %s results' %
                    (total, count))
            return True, list(map(lambda x: Sample(x, Config.ELAB_TIME_FORMAT), response['data']))
        else:
            return False, None


_VERIFY = Config.VERIFY_CERTIFICATE

_apiToken = None
_Core_Address = Config.CORE_ADDRESS
_jsonDecoder = JSONDecoder()
_py_requester = py_Requester()


def Login() -> bool:
    global _apiToken
    # dev
    print('# using temporary dev token, remember to change!')
    cred = open('credentials')
    cred.readline()
    cred.readline()
    _apiToken = cred.readline()
    return True

    ENDPOINT = 'auth/user'
    # todo: make login more secure
    credentials = open(Config.CREDENTIALS_PATH, 'r')
    def parseLine(): return credentials.readline().replace('\n', '')
    username = parseLine()
    password = parseLine()
    username, password = _readCredentials()

    if not username or not password:
        print('credential file error * note, make this more secure')
        return False

    body = {
        'username': username,
        'password': password
    }

    succeed, data = _sendRequest(
        Config.ELAB_URL, ENDPOINT, HttpMethod.POST, body=body)
    if succeed:
        print(data)
        _apiToken = data['token']
        print(_apiToken)
        return True
    else:
        return False


def _sendRequest(url: str, endpoint: str, method: HttpMethod, headers: dict = None, body: dict = None) -> Tuple[bool, dict]:
    fullurl = url + endpoint
    res = method.Send(fullurl, headers=headers, data=body)
    data = _jsonDecoder.decode(res.text)
    if res.status_code == 200:
        return True, data
    else:
        data['code'] = res.status_code
        return False, data


def _sendAuthenticatedRequest(url: str, endpoint: str, method: HttpMethod, body: dict = None) -> Tuple[bool, dict]:
    if _apiToken is not None:
        headers = {
            'Authorization': _apiToken
        }
        return _sendRequest(url, endpoint, method, headers, body)
    else:
        print('You must login first with `Limes.Login()`')
        return False, None

# print(Login())
# s, q = Query.ByAll('sample 12345')
# print(s)
# print(len(q))
# print(q[0]._raw)
