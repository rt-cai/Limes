from django.http import HttpResponse, JsonResponse
from django.core.handlers.wsgi import HttpRequest
from django.http.request import QueryDict
from django.middleware.csrf import get_token
from django.views.decorators.http import require_http_methods

from limes_common.models.network import server
from limes_common import config
from . import fileHandler


def _toDict(qd: QueryDict):
    d = {}
    for k, v in qd.items():
        d[k] = v
    return d

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
        self.Token = res.Token
        self.FirstName = res.FirstName
        self.LastName = res.LastName

_activeClients: dict[str, Client] = {}
_clientsByToken: dict[str, str] = {} # token: clientId

# these must match those in limes_common.models.network.endpoints

@require_http_methods(['GET'])
def Init(request: HttpRequest):
    return JsonResponse({config.CSRF_KEY: get_token(request)})

@require_http_methods(['POST'])
def Login(request: HttpRequest):
    SL = server.Login
    res = SL.Request(_toDict(request.POST))

    # remove old if exists
    old = _clientsByToken.get(res.Token)
    if old is not None: 
        _activeClients.pop(old)
        _clientsByToken.pop(res.Token)

    _activeClients[res.Id] = Client(res)
    _clientsByToken[res.Token] = res.Id

    print('login: %s' % (res.FirstName))
    return JsonResponse(SL.MakeResponse(True))

@require_http_methods(['POST'])
def Authenticate(request: HttpRequest):
    SA = server.Authenticate
    res = SA.Request(_toDict(request.POST))
    client = _activeClients.get(res.Id)
    success = client is not None
    token = client.Token if success else ''
    fName = client.FirstName if success else ''
    lName = client.LastName if success else ''
    print('auth: %s' % (fName if success else 'unknown'))
    return JsonResponse(SA.MakeResponse(success, token, fName, lName))

@require_http_methods(['POST'])
def Add(request: HttpRequest):
    SA = server.Add
    fail = lambda m='': JsonResponse(SA.MakeResponse(False, message=m))

    print('adding...')

    req = SA.Request(_toDict(request.POST))
    client = _activeClients.get(req.ClientId)
    if not client: return fail('Not logged in')

    success, msg = fileHandler.TryAddFile(client.Token, req.Meta, request.FILES[SA.FILE_KEY])
    if success:
        return JsonResponse(SA.MakeResponse(True, sampleName=msg))
    else:
        return fail(msg)

@require_http_methods(['POST'])
def Blast(request: HttpRequest):
    SB = server.Blast
    result = fileHandler.Blast(request.FILES[SB.FILE_KEY])
    return JsonResponse(SB.MakeResponse(True, result))
