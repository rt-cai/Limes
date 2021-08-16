from django.http import HttpResponse, JsonResponse
from django.core.handlers.wsgi import HttpRequest
from django.http.request import QueryDict
from django.middleware.csrf import get_token
from django.views.decorators.http import require_http_methods

from limes_common.models.network import Model, server
from limes_common import config
# from . import fileHandler

def _toRes(model: Model):
    return JsonResponse(model.ToDict())

# doesn't work
def _getClientIp(request: HttpRequest) -> str:
    x_forwarded_for = str(request.META.get('HTTP_X_FORWARDED_FOR'))
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    elif request.META.get('HTTP_X_REAL_IP'):
        ip = str(request.META.get('HTTP_X_REAL_IP'))
    else:
        ip = str(request.META.get('REMOTE_ADDR'))
    return ip

class Client:
    # todo: add timeout
    def __init__(self, res: server.Login.Request) -> None:
        self.Token = res.ELabKey
        self.FirstName = res.FirstName
        self.LastName = res.LastName

_activeClients: dict[str, Client] = {}
_clientsByToken: dict[str, str] = {} # token: clientId

# these must match those in limes_common.models.network.endpoints

@require_http_methods(['GET'])
def Init(request: HttpRequest):
    return _toRes(server.Init.Response(get_token(request)))

@require_http_methods(['POST'])
def Login(request: HttpRequest):
    SL = server.Login
    res = SL.Request.Load(request.body)
    # print(_toDict(request.POST))
    print(res.__dict__)

    # remove old if exists
    old = _clientsByToken.get(res.ELabKey)
    if old is not None: 
        _activeClients.pop(old)
        _clientsByToken.pop(res.ELabKey)

    if res.FirstName == '' or res.LastName == '':
        return _toRes(SL.Response(False))

    _activeClients[res.ClientId] = Client(res)
    _clientsByToken[res.ELabKey] = res.ClientId

    print('login: %s' % (res.FirstName))
    return _toRes(SL.Response(True))

@require_http_methods(['POST'])
def Authenticate(request: HttpRequest):
    SA = server.Authenticate
    res = SA.Request.Load(request.body)
    client = _activeClients.get(res.ClientId)
    success = client is not None
    token = ''
    fName = ''
    lName = ''
    if client is not None:
        token = client.Token
        fName = client.FirstName
        lName = client.LastName
    print('auth: %s' % (fName if success else 'unknown'))
    return _toRes(SA.Response(success, token, fName, lName))

@require_http_methods(['POST'])
def Add(request: HttpRequest):
    SA = server.Add
    fail = lambda m='': _toRes(SA.Response(False, message=m))

    print('adding not implimented')

    req = SA.Request.Load(request.body)
    client = _activeClients.get(req.ClientId)
    if not client: return fail('Not logged in')

    # success, msg = fileHandler.TryAddFile(client.Token, req.Meta, request.FILES[SA.FILE_KEY])
    success, msg = (False, 'not implemented with providers')
    if success:
        return _toRes(SA.Response(True, sampleName=msg))
    else:
        return fail(msg)

# @require_http_methods(['POST'])
# def Blast(request: HttpRequest):
#     SB = server.Blast
#     result = fileHandler.Blast(request.FILES[SB.FILE_KEY])
#     return JsonResponse(SB.MakeResponse(True, result))


@require_http_methods(['POST'])
def Search(request: HttpRequest):
    pass
# get data by sampleID?