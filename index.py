from http.server import BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import re

class handler(BaseHTTPRequestHandler):

    def do_GET(self):
        query = parse_qs(urlparse(self.path).query)

        def silent():
            self.send_response(204)
            self.end_headers()

        action = query.get("action", [None])[0]
        test1  = query.get("test1", [None])[0]

        if action != "api" or not test1:
            return silent()

        data = test1.lower()

        # ❌ Block spam / links / mentions
        blocked = ["@", "http", "https", "www", "salaar"]
        for b in blocked:
            if b in data:
                return silent()

        # ✅ Strict format (JK05F1806)
        pattern = re.compile(r"^[A-Z]{2}[0-9]{2}[A-Z][0-9]{4}$", re.I)
        if not pattern.match(test1):
            return silent()

        # ✅ Only valid response
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(
            bytes(
                f'{{"status":true,"result":"{test1}"}}',
                "utf-8"
            )
        )
