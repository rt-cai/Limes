bind = '10.0.0.224:8001'
# bind = 'sh-lims.microbiology.ubc.ca:8001'

workers = 1
max_requests = 1000
worker_class = 'geventwebsocket.gunicorn.workers.GeventWebSocketWorker'

CERT_DIR = 'server/certificate/certFiles'
certfile = '%s/cert.pem'%(CERT_DIR)
keyfile = '%s/key.pem'%(CERT_DIR)