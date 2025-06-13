#!/usr/bin/env python3

import argparse
import requests
import json
import sys
from common import splunk_common

def get_weather_data(city):
    """Get weather data from Open-Meteo API (no API key required)"""
    geocoding_url = f"https://geocoding-api.open-meteo.com/v1/search?name={city}&count=1"

    try:
        geo_response = requests.get(geocoding_url, timeout=5)
        if geo_response.status_code != 200:
            return {"error": f"Geocoding API failed: {geo_response.status_code}"}

        geo_data = geo_response.json()
        if not geo_data.get("results"):
            return {"error": f"City not found: {city}"}

        location = geo_data["results"][0]
        lat = location["latitude"]
        lon = location["longitude"]

        weather_url = (
            f"https://api.open-meteo.com/v1/forecast"
            f"?latitude={lat}&longitude={lon}"
            f"&current=temperature_2m,relative_humidity_2m,weathercode"
        )

        weather_response = requests.get(weather_url, timeout=5)
        if weather_response.status_code != 200:
            return {"error": f"Weather API failed: {weather_response.status_code}"}

        current = weather_response.json().get("current", {})

        return {
            "temperature": current.get("temperature_2m"),
            "humidity": current.get("relative_humidity_2m"),
            "weather_code": current.get("weathercode"),
            "lat": lat,
            "lon": lon
        }

    except Exception as e:
        return {"error": str(e)}

def main():
    parser = argparse.ArgumentParser(description="Fetch weather data and log it")
    parser.add_argument("--city", required=True, help="City name to fetch weather for")
    args = parser.parse_args()

    logger = splunk_common.setup_logging()

    data = get_weather_data(args.city)

    if "error" in data:
        splunk_common.log_json(logger, "ERROR", f"Weather fetch failed", {
            "city": args.city,
            "error": data["error"]
        })
        sys.exit(1)

    # Log success to Splunk internal logs
    splunk_common.log_json(logger, "INFO", "Weather fetch succeeded", {
        "city": args.city
    })

    # Output JSON to stdout for indexing
    print(json.dumps({
        "city": args.city,
        "temperature": data["temperature"],
        "humidity": data["humidity"],
        "weather_code": data["weather_code"],
        "lat": data["lat"],
        "lon": data["lon"]
    }))

if __name__ == "__main__":
    main()
