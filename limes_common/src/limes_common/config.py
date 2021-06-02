class Prod():
    VERIFY_CERTIFICATE = True
    KEEP_RAW_DATA = False
    ENCODING = 'utf-8'

class Dev(Prod):
    # VERIFY_CERTIFICATE = False
    KEEP_RAW_DATA = True

class ActiveGeneric(Dev):
    pass
# ---------------------------------------

class ProdCore(Prod):
    URL = '' # todo
    PORT = 0 # todo

class DevCore(ProdCore, Dev):
    URL = 'localhost'
    PORT = 3388

class ActiveCore(DevCore):
    pass
# ---------------------------------------


class ProdClient(Prod):
    CORE_ADDRESS = ProdCore.URL
    ELAB_URL = 'https://us.elabjournal.com/api/v1/'
    ELAB_TIME_FORMAT = '%Y-%m-%dT%H:%M:%SZ'

class DevClient(ProdClient, Dev):
    CORE_ADDRESS = '%s:%s/' % ('https://127.0.0.1', DevCore.PORT)
    CREDENTIALS_PATH = 'credentials' # todo: make more secure

class ActiveClient(DevClient):
    pass
# ---------------------------------------

class ProdProvider(Prod):
    CORE_ADDRESS = ProdCore.URL
    URL = '127.0.0.1'
    PORT = 3389

class DevProvider(ProdProvider, Dev):
    CORE_ADDRESS = DevClient.CORE_ADDRESS
    pass

class ActiveProvider(DevProvider):
    pass