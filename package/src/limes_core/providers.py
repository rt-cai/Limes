import json
import os
from typing import Union

from django.http import request

from limes_common import config
from limes_common.models.network import Model, ErrorModel, Primitive, server as Models
from limes_common.connections import Connection, Criteria
from limes_common.connections.ssh import SshConnection
# from limes_common.models.provider import Result as Result

# _registeredProviders: dict[str, ProviderConnection] = {}

def _loadStatics() -> dict[str, Connection]:
    with open(config.PROVIDER_STATICS_PATH, 'r') as raw:
        statics: list[dict] = json.loads("".join(raw.readlines()))
        loaded: dict[str, Connection] = {}

        availibleCriteria: dict[str, Criteria] = {}
        for c, v in [(k, x) for k, x in Criteria.__dict__.items() if k.isupper()]:
            availibleCriteria[c] = v

        for p in statics:
            # todo add these strings to some config
            name = p.get('name', '')
            type = p.get('type', None)
            url = p.get('url', '')
            if type == 'ssh':
                setup = p.get('setup', [])
                command = p.get('command', '')
                timeout = p.get('timeout', config.PROVIDER_DEFAULT_TRANSACTION_TIMEOUT)
                keepAlive = p.get('keepAlive', config.PROVIDER_DEFAULT_CONNECTION_TIMEOUT)
                criteria_strs = p.get('criterias', [])
                criterias = []
                for c in criteria_strs:
                    parsed = availibleCriteria.get(c, None)
                    if parsed is not None: criterias.append(parsed)
                if len(criterias) == 0:
                    criterias = [availibleCriteria[config.PROVIDER_DEFAULT_CRTIERIA]]
                loaded[name] = SshConnection(url, setup, command, timeout, keepAlive, criterias)
        if len(loaded) > 0:
            return loaded
    return {}
    # raise Exception('failed to load [%s]' % config.PROVIDER_STATICS_PATH)

class Handler:
    def __init__(self) -> None:
        self._providers: dict[str, Connection] = _loadStatics()

    def Handle(self, endpoint: str, raw: bytes) -> Model:
        method = 'Handle%s' % endpoint.title()
        myMethods = [m for m in dir(self) if m.startswith('Handle')]
        for m in myMethods:
            if m == method:
                return getattr(self, m)(raw)
        return ErrorModel(404, 'providers endpoint [%s] does not exist' % endpoint)

    def HandleList(self, raw: bytes):
        return Models.ListProviders.Response([
            Models.ProviderInfo(k, p.LastUse)
            for k, p in self._providers.items()
        ])

    def HandleSearch(self, raw: bytes):
        request = Models.Search.Request.Load(raw)

        def doSearch(name, p:Connection):
            p.Search(request.Query, request.Criteria)

        for name, provider in self._providers.items():
            if request.Criteria == []:
                doSearch(name, provider)
            else:
                for c in request.Criteria:
                    if c in provider.SearchableCriteria:
                        doSearch(name, provider)
            
        return Model()

    def HandleCall(self, raw: bytes):
        pass
    
# def _registerStatics():
#     recieveAddr, port = config.SERVER_BIND.split(':')
#     for p in statics.GetList(recieveAddr, int(port)):
#         _registerProvider(p)
#     pass
# _registerStatics()

# def QueryBySample(sampleId: str) -> Result:
#     # get list of providers from local "cache" (db?)
#     # ask each provider (multithread this to parallel network delay)
#     # aggregate results
#     return Result(False)

# def _registerProvider(p: ProviderConnection) -> Result:
#     if p.Name in _registeredProviders:
#         return Result(False, 'provider [%s] exists' % p.Name)
#     else:
#         status = p.CheckStatus()
#         if status.Success:
#             _registeredProviders[p.Name] = p
#         return status