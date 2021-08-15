from limes_provider.passive import ListenAsProvider, Handler

class FosDBHandler(Handler):
    pass
uri = "ws://localhost:8765"
ListenAsProvider(uri, FosDBHandler(), 3)