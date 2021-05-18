from limes_provider import HttpMethod, Provider, JsonResponse

_provider = Provider()
_provider.AddEndpoint('test', HttpMethod.GET, lambda r: JsonResponse({'from': 'le fosDB'}))
_provider.Start()