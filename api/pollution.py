from http.server import BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
from urllib.request import urlopen, Request
from urllib.error import URLError
import json
import os

API_KEY = os.environ.get("OPENWEATHER_API_KEY", "").strip().strip('\r\n\t ')
BASE_URL = "https://api.openweathermap.org/data/2.5"

AQI_CATEGORIES = {
    1: {"category": "Good", "color": "#4caf50"},
    2: {"category": "Fair", "color": "#8bc34a"},
    3: {"category": "Moderate", "color": "#ff9800"},
    4: {"category": "Poor", "color": "#ff4444"},
    5: {"category": "Very Poor", "color": "#b71c1c"},
}


def fetch_json(url):
    req = Request(url)
    with urlopen(req, timeout=10) as resp:
        return json.loads(resp.read().decode())


def build_response(lat, lon, city_name):
    data = fetch_json(
        f"{BASE_URL}/air_pollution?lat={lat}&lon={lon}&appid={API_KEY}"
    )

    entry = data["list"][0]
    aqi_val = entry["main"]["aqi"]
    comps = entry["components"]
    cat = AQI_CATEGORIES.get(aqi_val, AQI_CATEGORIES[3])

    return {
        "city": city_name,
        "aqi": aqi_val * 50,
        "category": cat["category"],
        "color": cat["color"],
        "pm2_5": round(comps.get("pm2_5", 0), 1),
        "pm10": round(comps.get("pm10", 0), 1),
        "co": round(comps.get("co", 0) / 1000, 2),
        "no2": round(comps.get("no2", 0), 1),
        "so2": round(comps.get("so2", 0), 1),
        "o3": round(comps.get("o3", 0), 1),
    }


class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        query = parse_qs(urlparse(self.path).query)
        lat = query.get("lat", [None])[0]
        lon = query.get("lon", [None])[0]
        city_name = query.get("name", ["Unknown"])[0]

        if not lat or not lon:
            self.send_response(400)
            self.send_header("Content-Type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(json.dumps({"error": "lat and lon required"}).encode())
            return

        try:
            data = build_response(lat, lon, city_name)
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(json.dumps(data).encode())
        except (URLError, KeyError, Exception) as e:
            self.send_response(500)
            self.send_header("Content-Type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(json.dumps({"error": str(e)}).encode())
