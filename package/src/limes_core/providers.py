from limes_provider import ProviderConnection
from limes_provider.passive import PassiveConnection
from limes_common.models.provider import Result as Result

_registeredProviders: dict[str, ProviderConnection] = {}

def QueryBySample(sampleId: str) -> Result:
    # get list of providers from local "cache" (db?)
    # ask each provider (multithread this to parallel network delay)
    # aggregate results
    return Result(False)

def _registerProvider(p: ProviderConnection) -> Result:
    if p.Name in _registeredProviders:
        return Result(False, 'provider [%s] exists' % p.Name)
    else:
        status = p.CheckStatus()
        if status.Success:
            _registeredProviders[p.Name] = p
        return status

def RegisterSSHProvider(name: str) -> Result:
    return _registerProvider(PassiveConnection(name))

def RegisterHTTPProvider() -> Result:
    return Result(False) # _registerProvider(HTTPProvider(name))