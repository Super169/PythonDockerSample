from http.server import HTTPServer, BaseHTTPRequestHandler
from io import BytesIO
from urllib.parse import urlparse, parse_qs

PORT = 8000

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):

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
print("Server is running at ", PORT)
httpd.serve_forever()