from json.decoder import JSONDecoder
from coms.requester import Requester
from coms.server import Server
from common.config import ActiveCore as Config
from models.network import Endpoints, ServerErrorResponse, HttpMethod, JsonResponse, Request
from models.inventory import Sample
from models.provider import RegistrationForm


class CoreServer(Server):
    def __init__(self):
        self._URL = Config.URL
        self._PORT = Config.PORT
        super().__init__(self._URL, self._PORT)

        self._Add('test', HttpMethod.GET, self._test)
        self._Add(Endpoints.REGISTER, HttpMethod.POST,
                  self._registerDataProvider)

        self._providers: list[RegistrationForm] = []
        self._requester = Requester()
        self._jsonDecoder = JSONDecoder()

    def _test(self, requst: Request):
        for f in self._providers:
            success, res = self._requester.SendRequest(
                'https://' + f.Address + '/', 'test', HttpMethod.GET)
            pass

        return JsonResponse(res)

    def _registerDataProvider(self, request: Request):
        success, body = request.TryGetJsonBody(self._jsonDecoder)
        if success:
            form = RegistrationForm(body)
            self._providers.append(form)
            return JsonResponse({})
        else:
            return ServerErrorResponse('failed to add provider')


class CoreRequester():
    def _verifyUser(self, token: str):
        pass

    def GetSample(self, sampleID: str) -> Sample:
        pass

    # def Search(self, method: SearchMethod, query: _Query) -> list[Sample]:
    #     pass


# this line must be last
cs = CoreServer()
cs.Serve()
