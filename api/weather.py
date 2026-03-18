from http.server import BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs, quote
from urllib.request import urlopen, Request
from urllib.error import URLError
from datetime import datetime
import json
import os

API_KEY = os.environ.get("OPENWEATHER_API_KEY", "").strip().strip('\r\n\t ')
BASE_URL = "https://api.openweathermap.org/data/2.5"

ICON_MAP = {
    "01": "sunny",
    "02": "partly_cloudy",
    "03": "cloudy",
    "04": "cloudy",
    "09": "rain",
    "10": "rain",
    "11": "storm",
    "13": "snow",
    "50": "cloudy",
}

DAY_NAMES = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]


def fetch_json(url):
    req = Request(url)
    with urlopen(req, timeout=10) as resp:
        return json.loads(resp.read().decode())


def map_icon(icon_code):
    return ICON_MAP.get(icon_code[:2], "cloudy")


def build_response(lat, lon, city_name):
    current = fetch_json(
        f"{BASE_URL}/weather?lat={lat}&lon={lon}&appid={API_KEY}&units=metric"
    )
    forecast_raw = fetch_json(
        f"{BASE_URL}/forecast?lat={lat}&lon={lon}&appid={API_KEY}&units=metric"
    )

    condition = current["weather"][0]["description"].title()
    icon_code = current["weather"][0]["icon"]

    # Build 5-day forecast — pick one entry per day (prefer 12:00)
    daily = {}
    for item in forecast_raw["list"]:
        date_part = item["dt_txt"].split(" ")[0]
        hour = item["dt_txt"].split(" ")[1]
        if date_part not in daily or hour == "12:00:00":
            daily[date_part] = item

    forecast_days = []
    for date_str in sorted(daily.keys())[:5]:
        item = daily[date_str]
        day_of_week = datetime.strptime(date_str, "%Y-%m-%d").weekday()
        forecast_days.append({
            "day": DAY_NAMES[day_of_week],
            "high": round(item["main"]["temp_max"]),
            "low": round(item["main"]["temp_min"]),
            "condition": item["weather"][0]["description"].title(),
            "icon": map_icon(item["weather"][0]["icon"]),
            "icon_code": item["weather"][0]["icon"],
        })

    wind_deg = current["wind"].get("deg", 0)
    directions = ["N", "NNE", "NE", "ENE", "E", "ESE", "SE", "SSE",
                   "S", "SSW", "SW", "WSW", "W", "WNW", "NW", "NNW"]
    wind_dir = directions[round(wind_deg / 22.5) % 16]

    return {
        "city": city_name,
        "temperature": round(current["main"]["temp"]),
        "feels_like": round(current["main"]["feels_like"]),
        "humidity": current["main"]["humidity"],
        "wind_speed": round(current["wind"]["speed"] * 3.6),
        "wind_gust": round(current["wind"].get("gust", 0) * 3.6),
        "wind_dir": wind_dir,
        "condition": condition,
        "condition_icon": map_icon(icon_code),
        "icon_code": icon_code,
        "pressure": current["main"]["pressure"],
        "visibility": round(current.get("visibility", 10000) / 1000),
        "clouds": current.get("clouds", {}).get("all", 0),
        "sunrise": current["sys"].get("sunrise", 0),
        "sunset": current["sys"].get("sunset", 0),
        "forecast": forecast_days,
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
