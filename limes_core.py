from inbound.server import Server
from network import HtmlResponse, Method, Request

class CoreServer(Server):
    _URL = 'localhost'
    _PORT = 3388

    def __init__(self):
        super().__init__(self._URL, self._PORT)

        def test(request: Request):
            res = ''
            for item in request.Headers.items():
                res += '%s: %s\n' % (item[0], item[1])
            return HtmlResponse('%s' % res)

        self._Add(['test', 'two'], Method.GET, test)


# this line must be last
cs = CoreServer()
cs.Serve()