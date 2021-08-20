from limes_provider.passive import Handler
from limes_common.models.network import provider as Models

class FosDBHandler(Handler):
    def OnStatusRequest(self, raw: str) -> Models.Status.Response:
        req = Models.Status.Request.Load(raw)
        return Models.Status.Response(True, req.Msg, 'Hello from FosDB!\n%s'%self._lastRawRequest)

FosDBHandler().HandleCommandLineRequest()