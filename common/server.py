from http.server import HTTPServer, BaseHTTPRequestHandler
import ssl

_URL = 'localhost'
_PORT = 3388

__CERTIFICATE_DIR = 'certificate/private/'
__KEY = 'key.pem'
__CERT= 'cert.pem'

# ===============================================================

_endpoints = {}

def Add(name, method, callback):
    _endpoints["%s - %s" % (name, method)] = callback

def Serve():
    server = HTTPServer((_URL, _PORT), BaseHTTPRequestHandler)

    server.socket = ssl.wrap_socket (server.socket, 
        keyfile=__CERTIFICATE_DIR + __KEY, 
        certfile=__CERTIFICATE_DIR + __CERT, server_side=True)

    server.serve_forever()