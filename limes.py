from models.inventory import Sample
from typing import Tuple, List
from common.config import ActiveClient as Config
from models.network import HttpMethod
from coms.requester import Requester
# from requests import Request as py_Requester

class Query():
    def ByAll(searchString: str) -> Tuple[bool, List[Sample]]:
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
_requester = Requester()
# _py_requester = py_Requester()


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

    if not username or not password:
        print('credential file error * note, make this more secure')
        return False

    body = {
        'username': username,
        'password': password
    }

    succeed, data = _requester.SendRequest(
        Config.ELAB_URL, ENDPOINT, HttpMethod.POST, body=body)
    if succeed:
        print(data)
        _apiToken = data['token']
        print(_apiToken)
        return True
    else:
        return False
def Test(endpoint: str, body: dict = None) -> Tuple[bool, dict]:
    return _sendAuthenticatedRequest(Config.CORE_ADDRESS, endpoint, HttpMethod.GET, body=body)

def _sendAuthenticatedRequest(url: str, endpoint: str, method: HttpMethod, body: dict = None) -> Tuple[bool, dict]:
    if _apiToken is not None:
        headers = {
            'Authorization': _apiToken
        }
        return _requester.SendRequest(url, endpoint, method, headers, body)
    else:
        print('You must login first with `Limes.Login()`')
        return False, None

# print(Login())
# s, q = Query.ByAll('sample 12345')
# print(s)
# print(len(q))
# print(q[0]._raw)
