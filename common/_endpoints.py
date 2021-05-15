from common.network import HttpMethod, Request, Response, ResponseType

class _abstractEndpoint:
    def _notImplimentedResponse(method: HttpMethod) -> Response:
        body = {
            'message': 'invalid [%s] endpoint' % (method)
        }
        return Response(404, ResponseType.JSON, body=body)

class _get(_abstractEndpoint):
    def Get(self, request: Request) -> Response:
        return self._notImplimentedResponse(HttpMethod.GET)

class _post(_abstractEndpoint):
    def Post(self, request: Request) -> Response:
        return self._notImplimentedResponse(HttpMethod.POST)

class _put(_abstractEndpoint):
    def Put(self, request: Request) -> Response:
        return self._notImplimentedResponse(HttpMethod.PUT)


class _query():
    class _sampleName(_get):
        def Get(self, request: Request) -> Response:
            return super().Get(request)

    def __init__(self) -> None:
        super().__init__()
        self.SampleName = self._sampleName()


class Api:
    def __init__(self) -> None:
        self.Query = _query()

