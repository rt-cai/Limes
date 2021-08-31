from __future__ import annotations

from limes_common.models import Model, Primitive, provider as Models
from limes_common.models import provider
from limes_common.models.provider import Transaction
from limes_common.models.endpoints import ServerEndpoint
from limes_common.models.http import GET, POST

class ServerRequest(Models.ProviderRequest):
    ClientId: str

class ServerResponse(Models.ProviderResponse):
    pass

class Init(Transaction):
    class Response(ServerResponse):
        CsrfToken: str
        def __init__(self, token: str = '') -> None:
            self.CsrfToken = token

class Authenticate(Transaction):
    class Request(ServerRequest):
        def __init__(self) -> None:
            super().__init__(ServerEndpoint.AUTHENTICATE.Path, GET)

    class Response(ServerResponse):
        Success: bool
        Token: str
        FirstName: str
        LastName: str

class Login(Transaction):
    class Request(ServerRequest):
        ELabKey: str
        FirstName: str
        LastName: str
        def __init__(self) -> None:
            super().__init__(ServerEndpoint.LOGIN.Path, POST)

    class Response(ServerResponse):
        Success: bool

class ProviderInfo(Model):
    Name: str
    LastUse: float
    Schema: provider.Schema

class List(Transaction):
    class Request(ServerRequest):
        def __init__(self) -> None:
            super().__init__(ServerEndpoint.LIST.Path, GET)

    class Response(ServerResponse):
        Providers: list[ProviderInfo]

class Search(Transaction):
    class Request(ServerRequest):
        Query: str
        Parameters: Primitive
        def __init__(self) -> None:
            super().__init__(ServerEndpoint.SEARCH.Path, POST)

    class Hit(Model):
        Type: str
        Data: Primitive

    class Response(ServerResponse):
        Hits: list[Search.Hit]

class CallProvider(Transaction):
    class Request(ServerRequest):
        ProviderName: str
        Body: Models.ProviderRequest
        def __init__(self) -> None:
            super().__init__(ServerEndpoint.CALL.Path, POST)

    class Response(ServerResponse):
        Body: Models.ProviderResponse
