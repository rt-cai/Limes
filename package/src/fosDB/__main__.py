from limes_common.connections.ssh import Handler
from limes_common.models import provider as Models, Primitive

class FosDB(Handler):
    def On_Schema_Request(self) -> Models.Schema:
        S = Models.Service
        return Models.Schema([
            S('Search', {'q': str}, {'r': str})
        ])

    def On_Generic_Request(self, endpoint: str, body: Primitive) -> Models.GenericResponse:
        res = Models.GenericResponse()
        res.Code = 200
        return res

# def SearchDemo():
#     pass

    # details()

FosDB().HandleCommandLineRequest()
# SearchDemo()