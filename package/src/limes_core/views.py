from django.http import HttpResponse, JsonResponse
from django.core.handlers.wsgi import HttpRequest
from django.middleware.csrf import get_token
from django.views.decorators.http import require_http_methods
from typing import TypeVar, Callable

from limes_common.models import Model, server
from limes_common import config
# from . import fileHandler
from . import providers

def _toRes(model: Model):
    return JsonResponse(model.ToDict())

# T = TypeVar('T')
# def _getReq(constr: Callable[..., T], req: HttpRequest) -> T:
#     return constr(req.body)

class Client:
    # todo: add timeout
    def __init__(self, res: server.Login.Request) -> None:
        self.Token = res.ELabKey
        self.FirstName = res.FirstName
        self.LastName = res.LastName

_activeClients: dict[str, Client] = {}
_clientsByToken: dict[str, str] = {} # token: clientId
_providers = providers.Handler()
# these must match those in limes_common.models.network.endpoints

@require_http_methods(['GET'])
def Init(request: HttpRequest):
    return _toRes(server.Init.Response(get_token(request)))

@require_http_methods(['POST'])
def Login(request: HttpRequest):
    SL = server.Login
    res = SL.Request.Parse(request.body)
    # print(_toDict(request.POST))

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
    elab_res = SA.Request.Parse(request.body)
    client = _activeClients.get(elab_res.ClientId)

    print('auth: %s' % (client.FirstName if client is not None else 'unknown'))
    res = SA.Response()
    if client is not None:
        res.Success = True
        res.Token = client.Token
        res.FirstName = client.FirstName
        res.LastName = client.LastName
    else:
        res.Success = False
    return _toRes(res)

# @require_http_methods(['POST'])
# def Add(request: HttpRequest):
#     SA = server.AddSample
#     fail = lambda m='': _toRes(SA.Response(False, message=m))

#     print('adding not implimented')

#     req = SA.Request.Parse(request.body)
#     client = _activeClients.get(req.ClientId)
#     if not client: return fail('Not logged in')

#     # success, msg = fileHandler.TryAddFile(client.Token, req.Meta, request.FILES[SA.FILE_KEY])
#     success, msg = (False, 'not implemented with providers')
#     if success:
#         return _toRes(SA.Response(True, sampleName=msg))
#     else:
#         return fail(msg)

@require_http_methods(['POST'])
def List(request: HttpRequest):
    return _toRes(_providers.HandleList(request.body))

@require_http_methods(['POST'])
def Reset(request: HttpRequest):
    return _toRes(_providers.Reset(request.body))

@require_http_methods(['POST'])
def Call(request: HttpRequest):
    return _toRes(_providers.HandleCall(request.body))

@require_http_methods(['POST'])
def Search(request: HttpRequest):
    res = _providers.HandleSearch(request.body)
    return _toRes(res)