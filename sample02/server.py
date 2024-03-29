from http.server import HTTPServer, BaseHTTPRequestHandler
from io import BytesIO
from urllib.parse import urlparse, parse_qs

PORT = 8000


class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):

    #  Refer to https://stackoverflow.com/questions/2617615/slow-python-http-server-on-localhost
    #  Override address_string can solve the issue in DNS lookup https://bugs.python.org/issue6085
    def address_string(self):
        host, port = self.client_address[:2]
        # return socket.getfqdn(host)
        return host

    #  Disable log_message
    #  Seems override address_string still cannot fix the issue,
    #  try to disable log_message as the bug is caused by the IP disabled in log_message.
    #  But it may have no effect if the IP is resolved somewhere before log_message.
    def log_message(self, format, *args):
        return

    def handler(self, mode, path, data):
        msg = 'mode: {}\nPath: {}\ndata: {}'.format(mode, path, data)
        self.send_response(200)
        self.end_headers()
        self.wfile.write(msg.encode())

    def do_GET(self):
        urlparm = urlparse(self.path) 
        path = urlparm.path
        data = parse_qs(urlparm.query)
        data['__success__'] = True
        self.handler('get', path, data)

    def do_POST(self):
        path = self.path
        CL = self.headers.get('Content-Length')
        if CL is not None:
            try:
                content_length = int(self.headers['Content-Length'])
                parm = self.rfile.read(content_length).decode()
                data = parse_qs(parm)
                data['__success__'] = True
            except:
                data = {'__success__': False, '__result__': 'Error reading parameters'}
        else:
            data = {'__success__': True, '__result__': 'No parameter'}
        self.handler('post', path, data)


# httpd = HTTPServer(('localhost', PORT), SimpleHTTPRequestHandler)
httpd = HTTPServer(('0.0.0.0', PORT), SimpleHTTPRequestHandler)
print("Server Sample02 is running at ", PORT)
httpd.serve_forever()