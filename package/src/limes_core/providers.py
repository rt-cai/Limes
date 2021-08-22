from limes_common import config
from limes_provider import ProviderConnection, statics
# from limes_common.models.provider import Result as Result

_registeredProviders: dict[str, ProviderConnection] = {}

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