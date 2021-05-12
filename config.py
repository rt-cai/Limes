class _Base:
    _URL_PREFIX = 'https://' 

class Production(_Base):
    CORE_URL = '' # todo
    CORE_PORT = 0 # todo
    _CORE_ADDRESS = CORE_URL
    CLIEN_VERIFY_CERTIFICATE = True

class Development(Production):
    CORE_URL = 'localhost'
    CORE_PORT = 3388
    _CORE_ADDRESS = '%s:%s' % ('127.0.0.1', CORE_PORT)
    CLIENT_VERIFY_CERTIFICATE = False

# other classes use Active for config settings
class Active(Development):
    def GetCoreAddress() -> str:
        return '%s%s' % (Active._URL_PREFIX, Active._CORE_ADDRESS)