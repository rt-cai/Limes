# bind = '127.0.0.1:8001'
bind = 'sh-lims.microbiology.ubc.ca:8001'

workers = 1 # todo: prevent multiple workers from spawning the same resources
worker_class = 'geventwebsocket.gunicorn.workers.GeventWebSocketWorker'