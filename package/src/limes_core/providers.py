import json
import os

from limes_common import config
from limes_common.models.network import Model, Primitive, server as Models
from limes_provider import ProviderConnection
from limes_provider.ssh import SshConnection
# from limes_common.models.provider import Result as Result

# _registeredProviders: dict[str, ProviderConnection] = {}

def _loadStatics() -> dict[str, ProviderConnection]:
    with open(config.PROVIDER_STATICS_PATH, 'r') as raw:
        statics: list[dict] = json.loads("".join(raw.readlines()))
        loaded: dict[str, ProviderConnection] = {}
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
                loaded[name] = SshConnection(url, setup, command, timeout, keepAlive)
        if len(loaded) > 0:
            return loaded
    raise Exception('failed to load [%s]' % config.PROVIDER_STATICS_PATH)

class Handler:
    def __init__(self) -> None:
        self._providers: dict[str, ProviderConnection] = _loadStatics()

    def Handle(self, endpoint: str, body: Primitive) -> Model:
        method = 'Handle%s' % endpoint.title()
        myMethods = [m for m in dir(self) if m.startswith('Handle')]
        for m in myMethods:
            if m == method:
                return getattr(self, m)(body)
        return Models.ErrorModel(404, 'providers endpoint [%s] does not exist' % endpoint)

    def HandleList(self, request):
        return Models.ListProviders.Response([
            Models.ProviderInfo(k, p.LastUse)
            for k, p in self._providers.items()
        ])

    def HandleSearch(self, request):
        pass

    def HandleCall(self, request):
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