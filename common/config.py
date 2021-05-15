class Prod():
    VERIFY_CERTIFICATE = True
    KEEP_RAW_DATA = False

class Dev():
    VERIFY_CERTIFICATE = False
    KEEP_RAW_DATA = True

class Prod_Core(Prod):
    CORE_URL = '' # todo
    CORE_PORT = 0 # todo

class Prod_Client(Prod):
    CORE_ADDRESS = Prod_Core.CORE_URL
    ELAB_URL = 'https://us.elabjournal.com/api/v1/'
    ELAB_TIME_FORMAT = '%Y-%m-%dT%H:%M:%SZ'

class Dev_Core(Prod_Core, Dev):
    URL = 'localhost'
    PORT = 3388

class Dev_Client(Prod_Client, Dev):
    CORE_ADDRESS = '%s:%s' % ('https://127.0.0.1', Dev_Core.PORT)
    CREDENTIALS_PATH = 'credentials' # todo: make more secure

# the currently active settings
class ActiveGeneric(Dev):
    pass

class ActiveCore(Dev_Core):
    pass

class ActiveClient(Dev_Client):
    pass