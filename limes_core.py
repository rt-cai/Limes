from inbound.server import Server

class CoreServer(Server):
    _URL = 'localhost'
    _PORT = 3388

    def __init__(self):
        super().__init__(self._URL, self._PORT)


# this line must be last
cs = CoreServer()
cs.Serve()