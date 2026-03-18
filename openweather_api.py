import requests
import json
import yaml
from datetime import datetime


# Set to True to use sample data (for demo/screenshot purposes)
# Set to False to use live API endpoints
DEMO_MODE = True

SAMPLE_COUNTRIES = [
    {"country_name": "pakistan", "country_symbol": "pk"},
    {"country_name": "united_states", "country_symbol": "us"},
    {"country_name": "united_kingdom", "country_symbol": "uk"},
    {"country_name": "india", "country_symbol": "in"},
    {"country_name": "saudi_arabia", "country_symbol": "sa"},
]

SAMPLE_FORECASTS = {
    "pakistan": {
        "temperature": "34°C",
        "feels_like": "38°C",
        "humidity": "62%",
        "wind_speed": "14 km/h",
        "weather_condition": "Partly Cloudy",
        "pressure": "1012 hPa",
        "visibility": "10 km",
        "forecast_summary": [
            {"day": "Wednesday", "high": "35°C", "low": "24°C", "condition": "Sunny"},
            {"day": "Thursday", "high": "33°C", "low": "23°C", "condition": "Partly Cloudy"},
            {"day": "Friday", "high": "30°C", "low": "21°C", "condition": "Rain Expected"},
        ]
    },
    "united_states": {
        "temperature": "18°C",
        "feels_like": "16°C",
        "humidity": "45%",
        "wind_speed": "22 km/h",
        "weather_condition": "Clear Sky",
        "pressure": "1018 hPa",
        "visibility": "16 km",
        "forecast_summary": [
            {"day": "Wednesday", "high": "20°C", "low": "10°C", "condition": "Clear"},
            {"day": "Thursday", "high": "22°C", "low": "12°C", "condition": "Sunny"},
            {"day": "Friday", "high": "19°C", "low": "9°C", "condition": "Cloudy"},
        ]
    },
    "united_kingdom": {
        "temperature": "11°C",
        "feels_like": "8°C",
        "humidity": "78%",
        "wind_speed": "30 km/h",
        "weather_condition": "Overcast",
        "pressure": "1005 hPa",
        "visibility": "8 km",
        "forecast_summary": [
            {"day": "Wednesday", "high": "12°C", "low": "6°C", "condition": "Rain"},
            {"day": "Thursday", "high": "10°C", "low": "5°C", "condition": "Showers"},
            {"day": "Friday", "high": "13°C", "low": "7°C", "condition": "Partly Cloudy"},
        ]
    },
    "india": {
        "temperature": "31°C",
        "feels_like": "36°C",
        "humidity": "70%",
        "wind_speed": "10 km/h",
        "weather_condition": "Haze",
        "pressure": "1008 hPa",
        "visibility": "5 km",
        "forecast_summary": [
            {"day": "Wednesday", "high": "33°C", "low": "25°C", "condition": "Haze"},
            {"day": "Thursday", "high": "34°C", "low": "26°C", "condition": "Sunny"},
            {"day": "Friday", "high": "32°C", "low": "24°C", "condition": "Thunderstorms"},
        ]
    },
    "saudi_arabia": {
        "temperature": "38°C",
        "feels_like": "40°C",
        "humidity": "20%",
        "wind_speed": "18 km/h",
        "weather_condition": "Clear Sky",
        "pressure": "1010 hPa",
        "visibility": "15 km",
        "forecast_summary": [
            {"day": "Wednesday", "high": "40°C", "low": "28°C", "condition": "Sunny"},
            {"day": "Thursday", "high": "41°C", "low": "29°C", "condition": "Clear"},
            {"day": "Friday", "high": "39°C", "low": "27°C", "condition": "Dusty"},
        ]
    },
}

SAMPLE_POLLUTION = {
    "pakistan": {
        "air_quality_index": 156,
        "category": "Unhealthy",
        "pm2_5": "78 µg/m³",
        "pm10": "125 µg/m³",
        "co_level": "1.2 mg/m³",
        "no2_level": "42 µg/m³",
        "so2_level": "18 µg/m³",
    },
    "united_states": {
        "air_quality_index": 42,
        "category": "Good",
        "pm2_5": "10 µg/m³",
        "pm10": "22 µg/m³",
        "co_level": "0.4 mg/m³",
        "no2_level": "15 µg/m³",
        "so2_level": "5 µg/m³",
    },
    "united_kingdom": {
        "air_quality_index": 58,
        "category": "Moderate",
        "pm2_5": "18 µg/m³",
        "pm10": "35 µg/m³",
        "co_level": "0.6 mg/m³",
        "no2_level": "28 µg/m³",
        "so2_level": "8 µg/m³",
    },
    "india": {
        "air_quality_index": 210,
        "category": "Very Unhealthy",
        "pm2_5": "120 µg/m³",
        "pm10": "195 µg/m³",
        "co_level": "2.1 mg/m³",
        "no2_level": "58 µg/m³",
        "so2_level": "30 µg/m³",
    },
    "saudi_arabia": {
        "air_quality_index": 95,
        "category": "Moderate",
        "pm2_5": "35 µg/m³",
        "pm10": "80 µg/m³",
        "co_level": "0.8 mg/m³",
        "no2_level": "22 µg/m³",
        "so2_level": "12 µg/m³",
    },
}


def get_weather_forecast(country_name):
    if DEMO_MODE:
        return SAMPLE_FORECASTS.get(country_name)

    try:
        response = requests.get(f"http://api.openweathermap.co/api/v3/weather/forecast/{country_name}")
        return response.json()
        
    except requests.exceptions.RequestException as e:
        print(f"Failed to fetch weather forcast for {country_name}. Error: {e}")
        return None


def get_countries():
    if DEMO_MODE:
        return SAMPLE_COUNTRIES

    try:
        response = requests.get("http://api.openweathermap.co/api/v3/countries")
        content_type = response.headers["Content-Type"]
        
        if content_type.startswith("application/json"):
            return json.loads(response.text)
        
        elif content_type.startswith("application/yaml"):
            return yaml.load(response.text, Loader=yaml.Loader)

    except requests.exceptions.RequestException as e:
        print(f"Failed to fetch list of supported countries. Error: {e}")
        return {}


def get_pollution_levels(country_name):
    if DEMO_MODE:
        return SAMPLE_POLLUTION.get(country_name)

    try:
        response = requests.get(f"http://api.openweathermap.co/api/v3/pollution/levels/{country_name}")
        return response.json()
        
    except requests.exceptions.RequestException as e:
        print(f"Failed to fetch pollution levels for {country_name}. Error: {e}")
        return None


def format_label(key):
    """Convert API keys to readable labels."""
    special = {
        "pm2_5": "PM2.5",
        "pm10": "PM10",
        "co_level": "CO Level",
        "no2_level": "NO2 Level",
        "so2_level": "SO2 Level",
        "air_quality_index": "Air Quality Index",
    }
    return special.get(key, key.replace("_", " ").title())


def format_weather_section(forecast, country_display):
    """Format weather forecast data into blog-friendly text."""
    lines = []
    lines.append(f"  Weather Forecast for {country_display}")
    lines.append("  " + "-" * 40)

    if isinstance(forecast, dict):
        for key, value in forecast.items():
            label = format_label(key)
            if isinstance(value, list):
                lines.append(f"  {label}:")
                for item in value:
                    if isinstance(item, dict):
                        for k, v in item.items():
                            lines.append(f"    - {format_label(k)}: {v}")
                        lines.append("")
                    else:
                        lines.append(f"    - {item}")
            elif isinstance(value, dict):
                lines.append(f"  {label}:")
                for k, v in value.items():
                    lines.append(f"    - {format_label(k)}: {v}")
            else:
                lines.append(f"  {label}: {value}")
    else:
        lines.append(f"  {forecast}")

    return "\n".join(lines)


def format_pollution_section(pollution, country_display):
    """Format pollution data into blog-friendly text."""
    lines = []
    lines.append(f"  Pollution Levels for {country_display}")
    lines.append("  " + "-" * 40)

    if isinstance(pollution, dict):
        for key, value in pollution.items():
            label = format_label(key)
            if isinstance(value, list):
                lines.append(f"  {label}:")
                for item in value:
                    if isinstance(item, dict):
                        for k, v in item.items():
                            lines.append(f"    - {format_label(k)}: {v}")
                        lines.append("")
                    else:
                        lines.append(f"    - {item}")
            elif isinstance(value, dict):
                lines.append(f"  {label}:")
                for k, v in value.items():
                    lines.append(f"    - {format_label(k)}: {v}")
            else:
                lines.append(f"  {label}: {value}")
    else:
        lines.append(f"  {pollution}")

    return "\n".join(lines)


def main():

    countries = get_countries()

    if not countries:
        print("Failed to fetch list of countries.")
        return

    if isinstance(countries, list):
        countries = {country['country_name']: country['country_symbol'] for country in countries}

    print("\nAvailable countries:")
    for idx, (country_name, country_symbol) in enumerate(countries.items(), start=1):
        print(f"{idx}. {country_name.replace('_', ' ').upper()}")

    try:
        selection = input("\nEnter the numbers of the countries you want to track, seperating each number with a comma: ")
        
        selected_indices = list(map(int, selection.split(',')))
        selected_countries = [list(countries.items())[i-1] for i in selected_indices]

        blog_output = []
        blog_output.append("=" * 50)
        blog_output.append("  WEATHER & POLLUTION REPORT")
        blog_output.append(f"  Generated: {datetime.now().strftime('%B %d, %Y at %I:%M %p')}")
        blog_output.append("=" * 50)

        for country_name, country_symbol in selected_countries:
            country_display = country_name.replace("_", " ").title()

            blog_output.append("")
            blog_output.append("*" * 50)
            blog_output.append(f"  {country_display} ({country_symbol.upper()})")
            blog_output.append("*" * 50)

            print(f"\nFetching {country_symbol.upper()} weather forecast...")
            forecast = get_weather_forecast(country_name)

            if forecast:
                blog_output.append("")
                blog_output.append(format_weather_section(forecast, country_display))

                print(f"Fetching {country_symbol.upper()} pollution levels...")
                pollution = get_pollution_levels(country_name)

                if pollution:
                    blog_output.append("")
                    blog_output.append(format_pollution_section(pollution, country_display))
                else:
                    blog_output.append("")
                    blog_output.append(f"  Pollution data unavailable for {country_display}.")
            else:
                blog_output.append("")
                blog_output.append(f"  Weather data unavailable for {country_display}.")

        blog_output.append("")
        blog_output.append("=" * 50)
        blog_output.append("  End of Report")
        blog_output.append("=" * 50)

        full_report = "\n".join(blog_output)

        # Print to terminal
        print("\n" + full_report)

        # Save to .txt file
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = f"weather_report_{timestamp}.txt"
        with open(filename, "w", encoding="utf-8") as f:
            f.write(full_report)

        print(f"\nReport saved to: {filename}")
        print("You can copy and paste the contents into your blog!")

    except ValueError:
        print("Invalid input! Please enter valid numbers.")
        return

if __name__ == "__main__":
    main()