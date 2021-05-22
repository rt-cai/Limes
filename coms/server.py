import os
from http.server import HTTPServer, BaseHTTPRequestHandler
import ssl
from typing import Callable

from models.network import HttpMethod, Request, Response, ErrorResponse, HtmlResponse, ResponseType
from common.config import ActiveGeneric as Config

class Server:
    class Node:
        def __init__(self):
            self.Endpoint = {}

    def __init__(self, url: str, port: int):
        package_directory = os.path.dirname(os.path.abspath(__file__))
        self.__CERTIFICATE_DIR = os.path.join(package_directory, 'certificate', 'private')
        self.__KEY = 'key.pem'
        self.__CERT= 'cert.pem'

        self._URL = url
        self._PORT = port

        self._endpoints = {}
        self._Add('', HttpMethod.GET, lambda _: HtmlResponse('LIMES Home'))

    def _Add(self, path: str, method: HttpMethod, callback: Callable[[Request], Response]):
        path = str(path)
        path = '/' + path
        print('endpoint [%s] added' % path)
        self._endpoints[self._toEndpointKey(path, method)] = callback

    def Serve(server):
        class Handler(BaseHTTPRequestHandler):
            # reduce verbose
            def send_response(self, code, message=None):
                self.send_response_only(code, message)

            # imporve latency
            def address_string(self) -> str:
                host, port = self.client_address[:2]
                #return socket.getfqdn(host)
                return host

            def do_GET(self):
                self._respond(HttpMethod.GET)
            def do_POST(self):
                self._respond(HttpMethod.POST)
            def do_PUT(self):
                self._respond(HttpMethod.PUT)

            def _respond(self, method: HttpMethod):
                valid, callback = server._getEndpoint(self.path, method)
                if valid:
                    rawHeaders = str(self.headers).split('\n')
                    headers = {}
                    for line in rawHeaders:
                        mid = line.find(': ')
                        headers[line[0:mid]] = line[mid+2:len(line)]

                    content_len = int(self.headers.get('Content-Length'))
                    rawBody = self.rfile.read(content_len)
                    # print(rawBody)
                    # print(self.headers)
                    response = callback(Request(headers, self.path, body=rawBody))
                else:
                    response = ErrorResponse(404, ResponseType.HTML, "endpoint doesn't exist! [%s:%s]" % (self.path, method))

                self.send_response(response.Code)
                self.send_header('Content-type',"text/%s" % response.Type)
                self.end_headers()
                self.wfile.write(bytes(response.Serialize(), Config.ENCODING))
        httpd = HTTPServer((server._URL, server._PORT), Handler)

        opj = os.path.join
        key_dir = opj(server.__CERTIFICATE_DIR, server.__KEY)
        cert_dir = opj(server.__CERTIFICATE_DIR, server.__CERT)
        httpd.socket = ssl.wrap_socket(httpd.socket, 
            keyfile=key_dir, 
            certfile=cert_dir,
            server_side=True)

        try:
            print('starting server at: %s\nport %s\n' % (server._URL, server._PORT))
            httpd.serve_forever()
        except KeyboardInterrupt:
            httpd.shutdown()
            print('\nserver closed')

    def _toEndpointKey(self, path: str, method: HttpMethod):
        return "%s:%s" % (method, path)

    def _getEndpoint(self, path: str, method: HttpMethod) -> Callable[[Request], Response]:
        key = self._toEndpointKey(path, method)
        print(key)
        if key in self._endpoints:
            return True, self._endpoints[key]
        else:
            return False, None
