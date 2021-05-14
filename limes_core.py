from inbound.server import Server
from common.config import ActiveCore as Config
from common.network import HtmlResponse, HttpMethod, Request, SampleResponse
from common.data import Sample
from outbound.requester import Requester

class CoreServer(Server):
    _URL = Config.CORE_URL
    _PORT = Config.CORE_PORT

    def __init__(self):
        super().__init__(self._URL, self._PORT)

        def test(request: Request):
            s = Sample()
            s.Name = 'charlie'
            return SampleResponse(s)

        self._Add('test', HttpMethod.GET, test)

class CoreRequester(Requester):
    def _verifyUser(self, token: str):
        pass

    def GetSample(self, sampleID: str) -> Sample:
        pass

    # def Search(self, method: SearchMethod, query: _Query) -> list[Sample]:
    #     pass

# this line must be last
cs = CoreServer()
cs.Serve()