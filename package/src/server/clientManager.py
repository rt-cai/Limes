from __future__ import annotations
import uuid

from limes_common.models.basic import AbbreviatedEnum

class ClientType(AbbreviatedEnum):
    ELAB = 1
    OTHER = 2

class Client:
    def __init__(self, FirstName, LastName, Token, Type: ClientType=ClientType.ELAB) -> None:
        self.Token = Token
        self.FirstName: str = FirstName
        self.LastName: str = LastName
        self.ClientID: str = '%012x' % (uuid.uuid1().int)
        self.Type: ClientType = Type

class ClientManager:
    I: ClientManager|None = None

    @classmethod
    def GetInstance(cls):
        if cls.I is None:
            cls.I = ClientManager()
        return cls.I

    def __init__(self) -> None:
        self._activeClients: dict[str, Client] = {}
        self._clientsByToken: dict[str, str] = {} # token: clientId

    def RegisterClient(self, client: Client) -> bool:
        # remove old if exists
        old = self._clientsByToken.get(client.Token)
        if old is not None: 
            self._activeClients.pop(old)
            self._clientsByToken.pop(client.Token)

        if client.FirstName is None or client.LastName is None:
            return False

        self._activeClients[client.ClientID] = client
        self._clientsByToken[client.Token] = client.ClientID

        return True

    def Get(self, clientId: str):
        # print(clientId, self._activeClients.keys())
        return self._activeClients.get(clientId, None)