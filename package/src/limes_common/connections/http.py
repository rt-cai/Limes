import requests as Requests
from limes_common.connections import Connection, Criteria

from limes_common.models.network.endpoints import Endpoint

class HttpConnection(Connection):
    def __init__(self, url, searchableCriteria: list[Criteria]) -> None:
        super().__init__(searchableCriteria)
        self.session = Requests.session()
        self._URL: str = url

    def _makeUrl(self, ep: Endpoint):
        return (self._URL if self._URL.endswith('/') else self._URL[:-1]) + ep.Path