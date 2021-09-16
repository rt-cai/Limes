import os

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
        sch.Code = 200
        return sch

    def On_Generic_Request(self, endpoint: str, body: Primitive) -> Models.GenericResponse:
        # self._send(MessageID(''), '>%s<, >%s<' % (endpoint, str(body)), True)
        res = Models.GenericResponse()

        def malformed():
            res.Code = 400
            res.Error = 'malformed request for [%s]' % endpoint
            return res

        if not isinstance(body, dict):
            return malformed()

        out: dict[str, Primitive] = {}
        if endpoint == 'sum':
            vals = body.get('values', [])
            if isinstance(vals, list):
                sum = 0
                for v in vals:
                    if isinstance(v, int) or isinstance(v, float):
                        sum += float(v)
                out = {'result': sum}
        elif endpoint == 'echo':
            out = {'echo': body.get('message', {})}
        elif endpoint == 'say hi':
            out = {'greeting': 'hello'}
        else:
            return malformed()

        res.Body = out
        return res

    def On_Search_Request(self, query: str) -> Models.Search.Response:
        res = Models.Search.Response()
        MINL = 3
        if len(query) < MINL:
            res.Code = 400
            res.Error = 'query [%s] must be at least %s characters' % (query, MINL)
            return res

        import numpy as np
        dataDir = 'test_provider/test_data'
        guagDir = '%s/prokka' % dataDir
        # k12Dir = '%s/ecoli_k12' % dataDir
        # g_ch: dict = np.load('%s/d_graph.npy' % k12Dir, allow_pickle=True).item()
        # sp_ch: dict = np.load('%s/d_species.npy' % k12Dir, allow_pickle=True).item()
        g_fos: dict = np.load('%s/d_graph.npy' % guagDir,allow_pickle=True).item()
        sp_fos: dict = np.load('%s/d_species.npy' % guagDir,allow_pickle=True).item()
        plate_sampleIDs: dict = np.load('%s/plate_sampleID.npy' % dataDir,allow_pickle=True).item()
        
        def search_reactions(graph: dict, sp: dict):
            reactions = []
            for v in graph.values():
                n = v.get('name', '').lower()
                if query in n:
                    d = {}
                    d['name'] = v['name']
                    d['reactants'] = [sp[i['species']]['name'] for i in v.get('listOfReactants', [])]
                    d['products'] = [sp[i['species']]['name'] for i in v.get('listOfProducts', [])]
                    samples = v.get('fbc:geneProductAssociation', [])
                    ids = set()
                    for s in samples:
                        tok = s['fbc:geneProduct'].split('_')
                        if len(tok) < 3: continue
                        lib, plate, well = tok[1:4]
                        sid = plate_sampleIDs.get(lib.upper(), {}).get(plate, None)
                        if sid is not None: ids.add(sid)
                    d['samples expressing function'] = list(ids)
                    reactions.append(d)
            return reactions

        def makeHit():
            h = Models.Search.Hit()
            h.Data = search_reactions(g_fos, sp_fos)
            h.DataType = str(dict)
            return h
        res.Hits = {
            'reactions': makeHit()
        }
        res.Code = 200
        return res

TestProvider().HandleCommandLineRequest()