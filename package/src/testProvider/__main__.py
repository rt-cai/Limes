from limes_common.connections.ssh import Handler, MessageID
from limes_common.models import Model, provider as Models, Primitive

class TestProvider(Handler):
    def On_Schema_Request(self) -> Models.Schema:
        sum = Models.Service()
        sum.Endpoint = 'sum'
        sum.Input = {'values': list[float]}
        sum.Output = {'result': float}
        
        echo = Models.Service()
        echo.Endpoint = 'echo'
        echo.Input = {'message': dict}
        echo.Output = {'echo': dict}

        hi = Models.Service()
        hi.Endpoint = 'say hi'
        hi.Output = {'greeting': str}

        sch = Models.Schema()
        sch.Services = [sum, echo, hi]
        return sch

    def On_Generic_Request(self, endpoint: str, body: Primitive) -> Primitive:
        # self._send(MessageID(''), endpoint+ str(body), True)
        res = 'error'
        if not isinstance(body, dict):
            return res

        out: dict[str, Models.Primitive] = {'code': '400'}
        if endpoint == 'sum':
            vals = body.get('values', [])
            if isinstance(vals, list):
                sum = 0
                for v in vals:
                    if isinstance(v, int) or isinstance(v, float):
                        sum += float(v)
                out = {'result': sum}
            res = endpoint
        elif endpoint == 'echo':
            out = {'echo': body.get('message', {})}
            res = endpoint
        elif endpoint == 'say hi':
            out = {'greeting': 'hello'}
            res = endpoint

        return out

TestProvider().HandleCommandLineRequest()