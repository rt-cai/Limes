class Prod():
    VERIFY_CERTIFICATE = True

class Dev():
    VERIFY_CERTIFICATE = False

class Prod_Core(Prod):
    CORE_URL = '' # todo
    CORE_PORT = 0 # todo

class Prod_Client(Prod):
    CORE_ADDRESS = Prod_Core.CORE_URL
    ELAB_URL = 'https://www.elabjournal.com/api/v1/'

class Dev_Core(Prod_Core, Dev):
    URL = 'localhost'
    PORT = 3388

class Dev_Client(Prod_Client, Dev):
    CORE_ADDRESS = '%s:%s' % ('https://127.0.0.1', Dev_Core.PORT)

# the currently active settings
class ActiveGeneric(Dev):
    pass

class ActiveCore(Dev_Core):
    pass

class ActiveClient(Dev_Client):
    pass