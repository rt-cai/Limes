from limes_common import config
from limes_common import models

from limes_common.connections.http import HttpConnection
from limes_common.models import Model, mmap as Models, provider as ProviderModels


class MmapConnection(HttpConnection):
    def __init__(self, oask: str) -> None:
        super().__init__(config.MMAP_URL)
        self._OASK = oask

    def _makeHeader(self):
        return {'Ocp-Apim-Subscription-Key': self._OASK}

    def SequencingFacilityQuery(self, barcode, status):
        transaction = Models.SequencingFacilityQuery
        req = transaction.Request()
        req.status = status
        req.barcode = barcode
        res = self._makeParseRequest(
            req,
            transaction.Response.Parse,
            transaction.Response()
        )
        return res
