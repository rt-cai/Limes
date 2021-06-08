from typing import Tuple, List
import os

from limes_common.connections import ELabConnection, ServerConnection
from limes_common.models.network import server

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

_server = ServerConnection()
_eLab = ELabConnection()

def _auth():
    res = _server.Authenticate()
    if res.Success:
        print('This terminal is logged in as %s' % res.FirstName)
        _eLab.SetToken(res.ELabKey)
    else:
        print('Not logged in')

def Login(username, password) -> bool:
    res = _eLab.Login(username, password)
    if res.Code not in [200, 401]:
        raise Exception('Failed to connect to eLab')

    if res.Success:
        _server.Login(res.Token, res.FirstName, res.LastName)
        print('logged in terminal as %s' % res.FirstName)
    return res.Success

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
    # if not username or not password:
    #     print('credential file error * note, make this more secure')
    #     return False

    # return _server.Login(username, password)
    return False

def Test() -> None:
#     f = open('delme', 'w')
#     f.close()
    # from limes_common.connections import ServerConnection
    # s = ServerConnection()
    # print(s.Authenticate())
    Login('phyberos@student.ubc.ca', 'sd43South27')

# def _sendAuthenticatedRequest(url: str, endpoint: str, method: HttpMethod, body: dict = None) -> Tuple[bool, dict]:
#     if _apiToken is not None:
#         headers = {
#             'Authorization': _apiToken
#         }
#         return SendRequest(url, endpoint, method, headers, str(body))
#     else:
#         print('You must login first with `Limes.Login()`')
#         return False, {}


# print(Login())
# s, q = Query.ByAll('sample 12345')
# print(s)
# print(len(q))
# print(q[0]._raw)
