from limes_common.models import Model, server

class Client:
    # todo: add timeout
    def __init__(self, res: server.RegisterClient.Request) -> None:
        self.Token = res.ELabKey
        self.FirstName = res.FirstName
        self.LastName = res.LastName

class ClientManager:
    def __init__(self) -> None:
        self._activeClients: dict[str, Client] = {}
        self._clientsByToken: dict[str, str] = {} # token: clientId

    def RegisterClient(self, client: server.RegisterClient.Request) -> bool:
        # remove old if exists
        old = self._clientsByToken.get(client.ELabKey)
        if old is not None: 
            self._activeClients.pop(old)
            self._clientsByToken.pop(client.ELabKey)

        if client.FirstName is None or client.LastName is None:
            return False

        self._activeClients[client.ClientID] = Client(client)
        self._clientsByToken[client.ELabKey] = client.ClientID

        return True

    def Get(self, clientId: str):
        return self._activeClients.get(clientId, None)