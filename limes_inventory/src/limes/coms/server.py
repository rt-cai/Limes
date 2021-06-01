import os
from http.server import HTTPServer, BaseHTTPRequestHandler
import ssl
from typing import Callable

from models.network import HttpMethod, Request, Response, ErrorResponse, HtmlResponse, ContentType
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
        self._Add('', HttpMethod.GET, lambda _: HtmlResponse('root'))

    def _Add(self, path: str, method: HttpMethod, callback: Callable[[Request], Response]):
        path = str(path)
        path = '/' + path
        key = self._toEndpointKey(path, method)
        # print(self._endpoints.keys())
        if key in self._endpoints.keys():
            status = 'updated'
        else:
            status = 'added'
        print('[%s] %s' % (path, status))
        self._endpoints[key] = callback

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
                    headersDict = {}
                    for line in rawHeaders:
                        mid = line.find(': ')
                        headersDict[line[0:mid]] = line[mid+2:len(line)]

                    clKey = 'Content-Length'
                    if not clKey in headersDict.keys():
                        content_len = 0
                    else:
                        content_len = int(headersDict[clKey])
                    rawBody = self.rfile.read(content_len)
                    # print(rawBody)
                    # print(self.headers)
                    response = callback(Request(headersDict, self.path, body=rawBody))
                    print('%s:%s' % (method, self.path))
                else:
                    # todo change this
                    response = ErrorResponse(404, ContentType.HTML, "endpoint doesn't exist! [%s:%s]" % (method, self.path))
                    print('-- 404 -- [%s]' % self.path)

                self.send_response(response.Code)
                self.send_header('Content-type', str(response.Type))
                self.end_headers()
                print(type(response.Bytes))
                print(type(response.Body))
                if not response.Bytes is None:
                    self.wfile.write(response.Bytes)
                else:
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

    def _getEndpoint(self, path: str, method: HttpMethod) -> 'tuple[bool, Callable[[Request], Response]]':
        sep = '/'
        tokens = path.split(sep)
        candidates = []
        candidate = ''
        for t in tokens:
            candidate += t + sep
            candidates.append(candidate + '*')
        candidates.append(path)
        candidates.reverse()
        for c in candidates:
            key = self._toEndpointKey(c, method)
            if key in self._endpoints:
                return True, self._endpoints[key]
        return False, None
