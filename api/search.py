from http.server import BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
from urllib.request import urlopen, Request
from urllib.error import HTTPError
import json
import os

API_KEY = os.environ.get("OPENWEATHER_API_KEY", "").strip()


class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        qs = parse_qs(urlparse(self.path).query)
        q = qs.get("q", [""])[0].strip()

        if not q or len(q) < 2:
            self._json({"results": []})
            return

        url = (
            f"http://api.openweathermap.org/geo/1.0/direct"
            f"?q={q}&limit=8&appid={API_KEY}"
        )
        try:
            req = Request(url)
            with urlopen(req, timeout=8) as resp:
                data = json.loads(resp.read().decode())

            seen = set()
            results = []
            for item in data:
                name = item.get("name", "")
                country = item.get("country", "")
                state = item.get("state", "")
                lat = round(item.get("lat", 0), 4)
                lon = round(item.get("lon", 0), 4)
                key = f"{name}-{country}-{round(lat,1)}-{round(lon,1)}"
                if key in seen:
                    continue
                seen.add(key)
                results.append({
                    "name": name,
                    "state": state,
                    "country": country,
                    "lat": lat,
                    "lon": lon,
                })
            self._json({"results": results})
        except HTTPError as e:
            self._json({"results": [], "error": f"HTTP {e.code}"})
        except Exception as e:
            self._json({"results": [], "error": str(e)})

    def _json(self, obj):
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(json.dumps(obj).encode())
