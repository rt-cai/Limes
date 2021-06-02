from typing import Tuple, List
import os

from .config import ActiveClient as Config
from .coms.requester import Requester
from .models.network import HttpMethod

# from  import Sample
# from models.network import HttpMethod
# from coms.requester import Requester
# from requests import Request as py_Requester


# class Query():
#     def ByAll(searchString: str) -> Tuple[bool, List[Sample]]:
#         ENDPOINT = 'samples'
#         endpointWithParam = '%s?search=%s' % (ENDPOINT, searchString)
#         succeed, response = _sendAuthenticatedRequest(
#             Config.ELAB_URL, endpointWithParam, HttpMethod.GET)
#         if succeed:
#             count = response['recordCount']
#             total = response['totalRecords']
#             if total > count:
#                 print('too many hits (%s total), truncated to %s results' %
#                     (total, count))
#             return True, list(map(lambda x: Sample(x, Config.ELAB_TIME_FORMAT), response['data']))
#         else:
#             return False, None


_VERIFY = Config.VERIFY_CERTIFICATE

_apiToken = None
_Core_Address = Config.CORE_ADDRESS
_requester = Requester()
# _py_requester = py_Requester()


def Login(username, password) -> bool:
    global _apiToken
    ENDPOINT = 'auth/user'

    # # dev-token
    # print('# using temporary dev token, remember to change!')
    # cred = open('credentials')
    # cred.readline()
    # cred.readline()
    # _apiToken = cred.readline()
    # return True

    # # dev-credentials-file
    # credentials = open(Config.CREDENTIALS_PATH, 'r')
    # def parseLine(): return credentials.readline().replace('\n', '')
    # username = parseLine()
    # password = parseLine()

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
        # print(data)
        _apiToken = data['token']
        # print(_apiToken)
        meta = data['user']
        fname = meta['firstName']
        lname = meta['lastName']
        print('logged in as %s %s' %(fname, lname))
        return True
    else:
        print('incorrect credentials')
        return False

def Test() -> None:
    f = open('delme', 'w')
    f.close()

def _sendAuthenticatedRequest(url: str, endpoint: str, method: HttpMethod, body: dict = None) -> Tuple[bool, dict]:
    if _apiToken is not None:
        headers = {
            'Authorization': _apiToken
        }
        return _requester.SendRequest(url, endpoint, method, headers, str(body))
    else:
        print('You must login first with `Limes.Login()`')
        return False, {}


# print(Login())
# s, q = Query.ByAll('sample 12345')
# print(s)
# print(len(q))
# print(q[0]._raw)
