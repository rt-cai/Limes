from http.server import HTTPServer, BaseHTTPRequestHandler
from network import Endpoint
import ssl
import os

class Server:
    _endpoints = {}

    def __init__(self, url: str, port: int):
        package_directory = os.path.dirname(os.path.abspath(__file__))
        self.__CERTIFICATE_DIR = os.path.join(package_directory, 'certificate', 'private')
        self.__KEY = 'key.pem'
        self.__CERT= 'cert.pem'

        self._URL = url
        self._PORT = port

    def _Add(self, endpoint: Endpoint):
        _endpoints["%s - %s" % (name, method)] = callback

    def Serve(self):
        class handler(BaseHTTPRequestHandler):
            def do_GET(self):
                self.send_response(200)
                self.send_header('Content-type','text/html')
                self.end_headers()

                message = "LIMES home"

                # need path parser
                print(self.path)
                # print(self.headers)

                self.wfile.write(bytes(message, "utf8"))

        httpd = HTTPServer((self._URL, self._PORT), handler)

        opj = os.path.join
        cert_dir = opj(self.__CERTIFICATE_DIR, self.__CERT)
        key_dir = opj(self.__CERTIFICATE_DIR, self.__KEY)
        httpd.socket = ssl.wrap_socket(httpd.socket, 
            keyfile=key_dir, 
            certfile=cert_dir,
            server_side=True)

        httpd.serve_forever()