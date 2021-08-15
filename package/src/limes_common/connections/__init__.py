import requests as Requests

from limes_common.models.network.endpoints import Endpoint

class Connection:
    def __init__(self, url) -> None:
        self.session = Requests.session()
        self._URL: str = url

    def _makeUrl(self, ep: Endpoint):
        return (self._URL if self._URL.endswith('/') else self._URL[:-1]) + ep.path