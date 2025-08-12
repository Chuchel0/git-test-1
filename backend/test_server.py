import http.server
import socketserver
import sys

PORT = 8000

class MyHttpRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/plain")
        self.end_headers()
        self.wfile.write(b"Hello, world!")

Handler = MyHttpRequestHandler

try:
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print("serving at port", PORT)
        httpd.serve_forever()
except OSError as e:
    print(f"Could not start server: {e}", file=sys.stderr)
    sys.exit(1)
