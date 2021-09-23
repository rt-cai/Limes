bind = '127.0.0.1:8001'
# bind = 'sh-lims.microbiology.ubc.ca:8001'

workers = 1
max_requests = 1000
worker_class = 'geventwebsocket.gunicorn.workers.GeventWebSocketWorker'