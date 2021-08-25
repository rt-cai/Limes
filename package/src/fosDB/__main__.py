from limes_common.connections.ssh import Handler
from limes_common.models.network import provider as Models

class FosDB(Handler):
    def OnStatusRequest(self, req: Models.Status.Request) -> Models.Status.Response:
        return Models.Status.Response(True, req.Msg, 'Hello from FosDB!')

    def OnSchemaRequest(self) -> Models.Schema:
        S = Models.Service
        return Models.Schema([
            S('search')
        ])

    def OnGenericRequest(self, purpose: str, req: dict[str, Models.Primitive]) -> Models.Generic:
        return Models.Generic('echo', req)

FosDB().HandleCommandLineRequest()