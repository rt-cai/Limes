from common.config import ActiveClient as Config
from common.network import HttpMethod
from outbound.requester import Requester

CREDENTIALS_PATH = 'credentials'
class ClientRequester(Requester):
    def __init__(self) -> None:
        super().__init__()
        self._apiToken = ''
        self._Core_Address = Config.CORE_ADDRESS

    def Login(self) -> str:
        ENDPOINT = 'auth/user'

        credentials = open(CREDENTIALS_PATH, 'r')
        username = credentials.readline()
        password = credentials.readline()

        if not username or not password:
            return None

        body = {
            'username': username,
            'password': password
        }
        res = self.MakeRequest(Config.ELAB_URL, ENDPOINT, HttpMethod.POST, body)
        print(res.status_code)
        print(res.text)
        return ''

r = ClientRequester()
r.Login()