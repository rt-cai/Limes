import requests as Requests
from typing import Callable, TypeVar, Union
import json

from .. import config
from ..utils import current_sec_time
from . import Connection
from ..models import Primitive, Model, provider as Models
from ..models.http import GET, POST, PATCH, PUT, DELETE

T = TypeVar('T')
class HttpConnection(Connection):
    def __init__(self, url) -> None:
        super().__init__()
        self.session = Requests.session()
        self._URL: str = url
        self.methods: dict[str, Callable[..., Requests.Response]] = {
            GET: self.session.get,
            POST: self.session.post,
            PATCH: self.session.patch,
            PUT: self.session.put,
            DELETE: self.session.delete
        }

    def _makeUrl(self, ep: str):
        return (self._URL if self._URL.endswith('/') else self._URL[:-1]) + ep

    def _makeJson(self, data: Models.ProviderRequest) -> dict:
        d = data.ToDict()
        return d

    def _makeHeader(self):
        return {}

    def _makeParams(self, req: Models.ProviderRequest):
        return req.QueryParams

    def _makeParseRequest(self, req: Models.ProviderRequest, parser: Callable[[dict, Models.ProviderResponse], T], default: T) -> T:
        raw = self.MakeRequest(req)
        if isinstance(raw.Body, dict):
            return parser(raw.Body, raw)
        else:
            return default

    def GetSchema(self) -> Models.Schema:
        s = Models.Schema()
        s.Code = 503
        s.Error = 'for static http providers, please refer to their specific documentation'
        return s

    def MakeRequest(self, request: Models.ProviderRequest) -> Models.GenericResponse:
        ep = request.TargetEndpoint
        doRequest = self.methods.get(request.Method.lower(), None)
        if ep is None or doRequest is None:
            msg = 'no endpoint given' if ep is None else 'bad http method [%s]'%request.Method
            return Models.GenericResponse({}, 0, msg)

        if isinstance(request, Models.GenericRequest):
            if isinstance(request.Body, dict):
                body = request.Body
            else:
                body = {'body': request.Body}
        else:
            body = self._makeJson(request)
        startTime = current_sec_time()
        res = doRequest(
            self._makeUrl(ep),
            json=body,
            headers = self._makeHeader(),
            params = self._makeParams(request),
            timeout = config.HTTP_TIMEOUT
        )
        
        code = res.status_code
        endTime = current_sec_time()
        try:
            body: dict[str, Primitive] = json.loads(res.text)
        except Exception:
            body = {'raw': res.text}
        report = Models.GenericResponse(body, code)
        report.ElapsedTime = endTime - startTime
        return report