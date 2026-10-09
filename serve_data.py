"""
Tiny local API that serves the experiment data as JSON.

Run:  python serve_data.py
Then: http://127.0.0.1:8000/api/ab_test
"""
from http.server import BaseHTTPRequestHandler, HTTPServer

import pandas as pd

PORT = 8000
DATA = pd.read_csv("raw_ab_test.csv").to_json(orient="records")  # NaN -> null


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/api/ab_test":
            body = DATA.encode()
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
        else:
            self.send_response(404)
            self.end_headers()


if __name__ == "__main__":
    print(f"Serving on http://127.0.0.1:{PORT}/api/ab_test  (Ctrl+C to stop)")
    HTTPServer(("127.0.0.1", PORT), Handler).serve_forever()
