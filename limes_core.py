from network.server import Server
from common.config import ActiveCore as Config
from models.network import HtmlResponse, HttpMethod, Request, SampleResponse
from models.inventory import Sample

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
        self._Add('register', HttpMethod.POST, self._registerDataSource)

    def _registerDataSource(self, request: Request):
        pass

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