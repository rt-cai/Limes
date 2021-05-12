import os
from http.server import HTTPServer, BaseHTTPRequestHandler
import ssl
from typing import Callable

from network import Method, Request, _Response, ErrorResponse, HtmlResponse

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
        self._Add([], Method.GET, lambda _: HtmlResponse('LIMES Home'))

    def _Add(self, path: list[str], method: Method, callback: Callable[[Request], _Response]):
        pathStr = '/%s' % ('/'.join(path))
        print('endpoint [%s] added' % pathStr)
        self._endpoints[self._toEndpointKey(pathStr, method)] = callback

    def Serve(server):
        class Handler(BaseHTTPRequestHandler):
            # reduce verbose
            def send_response(self, code, message=None):
                self.send_response_only(code, message)

            def do_GET(self):
                self._respond(Method.GET)

            def _respond(self, method: Method):
                valid, callback = server._getEndpoint(self.path, method)
                if valid:
                    rawHeaders = str(self.headers).split('\n')
                    headers = {}
                    for line in rawHeaders:
                        mid = line.find(': ')
                        headers[line[0:mid]] = line[mid+2:len(line)]
                    print(self.headers)
                    response = callback(Request(headers, self.path))
                else:
                    response = ErrorResponse(404, "endpoint [%s] for [%s] request not found!" % (self.path, method))

                self.send_response(response.Code)
                self.send_header('Content-type',"text/%s" % response.Type)
                self.end_headers()
                self.wfile.write(bytes(response.Body, 'utf8'))
        httpd = HTTPServer((server._URL, server._PORT), Handler)

        opj = os.path.join
        cert_dir = opj(server.__CERTIFICATE_DIR, server.__CERT)
        key_dir = opj(server.__CERTIFICATE_DIR, server.__KEY)
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

    def _toEndpointKey(self, path: str, method: Method):
        return "%s:%s" % (method, path)

    def _getEndpoint(self, path: str, method: Method) -> Callable[[Request], _Response]:
        key = self._toEndpointKey(path, method)
        print(key)
        if key in self._endpoints:
            return True, self._endpoints[key]
        else:
            return False, None
