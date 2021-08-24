from limes_provider.ssh import Handler
from limes_common.models.network import Model, provider as Models

class TestProvider(Handler):
    def OnStatusRequest(self, req: Models.Status.Request) -> Models.Status.Response:
        return Models.Status.Response(True, req.Msg, 'Hello from the test Provider!')

    def OnSchemaRequest(self) -> Models.Schema:
        S = Models.Service
        return Models.Schema([
            S('sum', {'values': list[float]}, {'result': float}),
            S('echo', {'message': dict}, {'echo': dict}),
            S('say hi', {}, {'greeting': str})
        ])

    def OnGenericRequest(self, purpose: str, data: dict[str, Models.Primitive]) -> Models.Generic:
        res = 'error'
        out: dict[str, Models.Primitive] = {'code': '400'}
        if purpose == 'sum':
            vals = data.get('values', [])
            if isinstance(vals, list):
                sum = 0
                for v in vals:
                    if isinstance(v, int) or isinstance(v, float):
                        sum += float(v)
                out = {'result': sum}
            res = purpose
        elif purpose == 'echo':
            out = {'echo': data.get('message', {})}
            res = purpose
        elif purpose == 'say hi':
            out = {'greeting': 'hello'}
            res = purpose


        return Models.Generic(res, out)

TestProvider().HandleCommandLineRequest()