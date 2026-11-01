import csv
import io
import json
from pathlib import Path
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer

ROOT = Path(__file__).resolve().parent

class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(ROOT), **kwargs)

    def do_GET(self):
        if self.path.split('?')[0] == '/api/datasets':
            result = []
            for path in sorted((ROOT / 'data').glob('*.csv')):
                meta = path.with_suffix('.legend.json')
                result.append({'file': path.name, 'meta': json.loads(meta.read_text('utf-8-sig')) if meta.exists() else {'title': path.stem, 'unit': '', 'sample': False}})
            payload = json.dumps(result, ensure_ascii=False).encode()
            self.send_response(200)
            self.send_header('Content-Type', 'application/json; charset=utf-8')
            self.send_header('Cache-Control', 'no-store')
            self.end_headers()
            self.wfile.write(payload)
        else:
            super().do_GET()

if __name__ == '__main__':
    print('서울 데이터 지도: http://localhost:8000', flush=True)
    ThreadingHTTPServer(('127.0.0.1', 8080), Handler).serve_forever()
