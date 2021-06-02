from coms.requester import Requester
from coms.server import Server
from common.config import ActiveCore as Config
from models.basic import AdvancedEnum, PublicOnlyDict
from models.network import HtmlResponse, HttpMethod, JsonResponse, Request
from models.inventory import Sample
from models.provider import RegistrationForm
from website.handler import Pages, ServeFolder

class Endpoints(AdvancedEnum):
    REGISTER = 1, RegistrationForm

    def __init__(self, _: int, data: PublicOnlyDict) -> None:
        self.DataModel = data

    def __str__(self) -> str:
        default = super().__str__()
        start = default.find(self.name)
        return default[start:].lower()

class CoreServer(Server):
    def __init__(self):
        self._URL = Config.URL
        self._PORT = Config.PORT
        super().__init__(self._URL, self._PORT)

        self._Add('test', HttpMethod.GET, self._test)
        self._Add('', HttpMethod.GET, self._serveHome)
        self._Add('sleep', HttpMethod.GET, self._serveSleep)
        for folder in ['lib', 'src', 'res']:
            self._Add('%s/*'%folder, HttpMethod.GET, ServeFolder())

        self._requester = Requester()

    def _serveHome(self, request: Request):
        page = Pages.HOME.GetPage()
        return HtmlResponse(page)
        
    def _serveSleep(self, req: Request):
        page = Pages.SLEEP.GetPage()
        return HtmlResponse(page)

    def _test(self, requst: Request):
        for f in self._providers:
            success, res = self._requester.SendRequest(
                'https://' + f.Address + '/', 'test', HttpMethod.GET)
            pass

        return JsonResponse(res)


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
