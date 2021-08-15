from io import BufferedReader
from typing import Any, Union
import os
from functools import reduce
from requests.exceptions import ConnectionError

from paramiko import file
from limes.tools.qol import Switch

from limes_common.connections.eLab import ELabConnection
from limes_common.connections.server import ServerConnection
from limes_common.models.network import server
from limes_common.models.network.elab import SampleModel

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

class Limes:
    def __init__(self) -> None:
        self._server = ServerConnection()
        self._eLab = ELabConnection()

    #   def _auth() -> tuple[bool, str]:
    def _auth(self) -> bool:
        res = self._server.Authenticate()
        if res.Success:
            print('Authenticated terminal as %s' % res.FirstName)
            # return True, res.FirstName
            self._eLab.SetToken(res.ELabKey)
        else:
            # return False, ''
            print('Not logged in')
        return res.Success
                

    def Login(self, username, password) -> bool:
        if not self._server.Ready: return False
        res = self._eLab.Login(username, password)
        if res.Code not in [200, 401]:
            raise Exception('Failed to connect to eLab')

        if res.Success:
            self._server.Login(res.Token, res.FirstName, res.LastName)
            print('logged in terminal as %s' % res.FirstName)
        return res.Success

    # class UnrecognizedCriteriaException(Exception):
    #     pass
    # SEARCH_CRITERIA_LIST = list(c.lower() for c in ['sampleID', 'name'])
    # def Search(params: dict[str, list[str]]):
    #     params = dict((k.lower(), v) for k, v in params.items())
    #     invalids = list(filter(lambda p: p not in SEARCH_CRITERIA_LIST, params.keys()))
    #     if len(invalids) > 0:
    #         raise UnrecognizedCriteriaException('unrecognized criteria: %s' % \
    #             reduce(lambda s, c: '%s, [%s]' % (s, c), invalids[1:], '[%s]' %invalids[0]))

    #     switcher = {
    #         'sampleid': self._eLab.SearchSamplesById
    #     }

    #     # todo, this should go in main, return dict here
    #     # todo value check
    #     try:
    #         res = list(switcher[k](v) for k, v in params.items())
    #     except ValueError as err:
    #         return err
    #     # todo: AND and OR logic
    #     # todo: save result as csv
    #     res = res[0] # temp since only one criteria so far
    #     count = len(res.Samples)
    #     msg = '%s result%s found' % (count, 's' if count != 1 else '')
    #     max = 5
    #     i = 1
    #     for sample in res.Samples:
    #         msg += '\n\n%s of %s' % (i, count)
    #         msg += '\nID: %s\nName: %s' % (sample.Id, sample.Name)
    #         i += 1
    #         if i > max: break
    #     return msg

    def Search(self, token: str) -> list[SampleModel]:
        res = self._eLab.SearchSamples(token)
        return res.Samples

    def Add(self, sampleId: str, path: str, fileName: str=None) -> bool:
        if not self._server.Ready: return False

        if fileName is None:
            tokens = path.split('/')
            fileName = tokens[len(tokens) - 1]

        path = os.path.abspath(path)
        file = open(path, 'rb')
        res = self._server.Add(sampleId, path, fileName, file)

        if not res.Success:
            print(res.Message)
        else:
            print('file [%s] added to sample [%s]' % (fileName, res.SampleName))
        return res.Success

    def Blast(self, queryPath: str) -> str:
        try:
            query = open(queryPath, 'rb')
            res = self._server.Blast(query)
            return res.Result
        except:
            print('[%s] not found' % (queryPath))
        return ''

    def dLogin(self) -> None:
        with open('../../credentials/elab') as cred:
            lines = cred.readlines()
            lines = list(map(lambda l: l.replace('\n', ''), lines))
            if not self.Login(lines[0], lines[1]):
                print('quick login failed')
                
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
