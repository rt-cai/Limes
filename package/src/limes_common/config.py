# CSRF_NAME = 'csrfmiddlewaretoken'
CSRF_NAME = 'X-CSRFToken'

ELAB_URL = 'https://us.elabjournal.com/'
# ELAB_URL = 'https://elab.msl.ubc.ca/'
ELAB_API = '%sapi/v1/' % ELAB_URL

SERVER_API_VER = 'd1'
SERVER_BIND = 'sh-lims.microbiology.ubc.ca:8001'
SERVER_URL = 'http://%s/api/%s/' % (SERVER_BIND, SERVER_API_VER)
SERVER_DB_PATH = 'limes_server/db'

SHAMWOW_URL = 'shamwow.microbiology.ubc.ca'

ENCODING = 'utf-8'
            
SSH_TIMEOUT = 10