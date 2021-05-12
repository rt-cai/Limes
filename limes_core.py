from inbound.server import Server
from common import HtmlResponse, HttpMethod, Request, Sample, SampleResponse
from config import Active as Config
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

# this line must be last
cs = CoreServer()
cs.Serve()