from django.http import HttpResponse, JsonResponse
from django.core.handlers.wsgi import HttpRequest
from django.http.request import QueryDict
from django.middleware.csrf import get_token
from django.views.decorators.http import require_http_methods
from django.core.files.storage import default_storage

from limes_common.models.network import server
from limes_common import config

from limes_common.connections import ELabConnection

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


def _fsPath(clientId, file):
    return '%s/%s/%s' % (config.SERVER_DB_PATH, clientId, file)

# these must match those in limes_common.models.network.endpoints

@require_http_methods(['GET'])
def Init(request: HttpRequest):
    return JsonResponse({config.CSRF_KEY: get_token(request)})

@require_http_methods(['POST'])
def Login(request: HttpRequest):
    SL = server.Login
    res = SL.Request(_toDict(request.POST))
    _activeClients[res.Id] = Client(res)
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
    return JsonResponse(SA.MakeResponse(success, token, fName, lName))

@require_http_methods(['POST'])
def Add(request: HttpRequest):
    SA = server.Add
    response = lambda s, m='': JsonResponse(SA.MakeResponse(s, m))

    req = SA.Request(_toDict(request.POST))
    client = _activeClients.get(req.ClientId)
    if not client: return response(False, 'Not logged in')

    ec = ELabConnection()
    ec.SetToken(client.Token)
    sampleRes = ec.GetSample(req.SampleId)
    if sampleRes.Code != 200: return response(False, 'Sample [%s] not found' % (req.SampleId))
    sample = sampleRes.Sample


    fsPath = _fsPath(sample.Id, req.FileName)
    if default_storage.exists(fsPath): 
        return response(False, 'File [%s] already exists for sample [%s]' % (req.FileName, sample.Id))

    try:
        file = request.FILES[SA.FILE_KEY]
        default_storage.save(fsPath, file)
    except Exception as err:
        return JsonResponse(SA.MakeResponse(False, str(err)))

    return JsonResponse(SA.MakeResponse(True))
