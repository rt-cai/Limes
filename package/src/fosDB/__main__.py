from limes_provider.ssh import Handler
from limes_common.models.network import provider as Models

class FosDBHandler(Handler):
    def OnStatusRequest(self, raw: str) -> Models.Status.Response:
        req = Models.Status.Request.Load(raw)
        return Models.Status.Response(True, req.Msg, 'Hello from FosDB!\n%s'%self._lastRawRequest)

    def OnSchemaRequest(self) -> Models.Schema:
        S = Models.Service
        return Models.Schema([
            S('s1')
        ])

    def OnGenericRequest(self, req: dict) -> Models.Generic:
        return Models.Generic({
            'echo': req
        })

FosDBHandler().HandleCommandLineRequest()