import ssl
import http.server
from http.server import BaseHTTPRequestHandler
import os

server_address = ('0.0.0.0', 8080)

class Handler(BaseHTTPRequestHandler):
    def send_response(self, *args, **kwargs):
        BaseHTTPRequestHandler.send_response(self, *args, **kwargs)
        self.send_header('Access-Control-Allow-Origin', '*')
        #response headers
        print(self.headers)
    def do_POST(self):
        """Save a file following a HTTP PUT request"""
        filename = os.path.basename(self.path)
        # Don't overwrite files
        if os.path.exists(filename):
            self.send_response(409, 'Conflict')
            self.end_headers()
            reply_body = '"%s" already exists\n' % filename
            self.wfile.write(reply_body.encode('utf-8'))
            return

        file_length = int(self.headers['Content-Length'])
        with open(filename, 'wb') as output_file:
            output_file.write(self.rfile.read(file_length))
        self.send_response(201, 'Created')
        self.end_headers()
        reply_body = 'Saved "%s"\n' % filename
        self.wfile.write(reply_body.encode('utf-8'))


httpd = http.server.HTTPServer(server_address, Handler)
httpd.socket = ssl.wrap_socket(httpd.socket, server_side=True, certfile='/home/cert.crt', keyfile='/home/pkey.pem',  ssl_version=ssl.PROTOCOL_TLS)
httpd.serve_forever()
