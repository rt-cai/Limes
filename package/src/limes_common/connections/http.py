import requests as Requests
from typing import Callable, TypeVar, Union
import json

from limes_common.models.basic import AbbreviatedEnum
from limes_common.connections import Connection
from limes_common.models import Primitive, Model, provider as Models
from limes_common.models.http import GET, POST

T = TypeVar('T')
class HttpConnection(Connection):
    def __init__(self, url) -> None:
        super().__init__()
        self.session = Requests.session()
        self._URL: str = url
        self.methods: dict[str, Callable[..., Requests.Response]] = {
            GET: self.session.get,
            POST: self.session.post
        }

    def _makeUrl(self, ep: str):
        return (self._URL if self._URL.endswith('/') else self._URL[:-1]) + ep

    def _makeJson(self, data: Model) -> dict:
        d = data.ToDict()
        return d

    def _makeHeader(self):
        return {}

    def MakeRequest(self, request: Models.ProviderRequest) -> Models.GenericResponse:
        ep = request._TargetEndpoint
        doRequest = self.methods.get(request._Method, None)
        if ep is None or doRequest is None:
            return Models.GenericResponse({}, 0, 'failed to reach server')
        
        res = doRequest(
            self._makeUrl(ep),
            json=self._makeJson(request),
            headers = self._makeHeader()
        )

        code = res.status_code
        try:
            body: dict[str, Primitive] = json.loads(res.text)
        except Exception:
            body = {'raw': res.text}
        return Models.GenericResponse(body, code)