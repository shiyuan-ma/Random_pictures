from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parent
UPSTREAM = 'https://veil.ortlinde.com'


def build_upstream_url(path: str, query: str = '') -> str:
    url = f'{UPSTREAM}{path}'
    if query:
        url = f'{url}?{query}'
    return url


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed = urlparse(self.path)

        if parsed.path == '/api/random':
            self.send_response(302)
            self.send_header('Location', build_upstream_url('/v1/random', parsed.query))
            self.send_header('Cache-Control', 'no-store')
            self.end_headers()
            return

        if parsed.path.startswith('/api/image/'):
            image_id = parsed.path.removeprefix('/api/image/')
            self.send_response(302)
            self.send_header('Location', build_upstream_url(f'/v1/image/{image_id}', parsed.query))
            self.send_header('Cache-Control', 'no-store')
            self.end_headers()
            return

        if parsed.path == '/api/meta':
            self.send_response(302)
            self.send_header('Location', build_upstream_url('/v1/random/meta', parsed.query))
            self.send_header('Cache-Control', 'no-store')
            self.end_headers()
            return

        if parsed.path == '/' or parsed.path == '/index.html':
            html = (ROOT / 'index.html').read_bytes()
            self.send_response(200)
            self.send_header('Content-Type', 'text/html; charset=utf-8')
            self.send_header('Cache-Control', 'no-store')
            self.end_headers()
            self.wfile.write(html)
            return

        self.send_error(404)

    def log_message(self, format, *args):
        pass


if __name__ == '__main__':
    server = ThreadingHTTPServer(('127.0.0.1', 8000), Handler)
    print('Serving on http://127.0.0.1:8000', flush=True)
    server.serve_forever()
