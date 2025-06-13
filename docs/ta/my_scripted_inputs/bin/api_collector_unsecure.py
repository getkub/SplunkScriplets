#!/usr/bin/env python3

import argparse
import requests
import json
import sys
from common import splunk_common

def get_weather_data(city):
    """Get weather data from Open-Meteo API (no API key required)"""
    # First get coordinates for the city using geocoding API
    geocoding_url = f"https://geocoding-api.open-meteo.com/v1/search?name={city}&count=1"
    
    try:
        # Get coordinates
        geo_response = requests.get(geocoding_url, timeout=5)
        if geo_response.status_code == 200:
            geo_data = geo_response.json()
            if not geo_data.get('results'):
                return {'error': f"City not found: {city}"}
            
            location = geo_data['results'][0]
            lat = location['latitude']
            lon = location['longitude']
            
            # Get weather data using coordinates
            weather_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current=temperature_2m,relative_humidity_2m,weather_code,wind_speed_10m"
            weather_response = requests.get(weather_url, timeout=5)
            
            if weather_response.status_code == 200:
                weather_data = weather_response.json()
                current = weather_data['current']
                
                # Map weather codes to descriptions
                weather_codes = {
                    0: "Clear sky",
                    1: "Mainly clear",
                    2: "Partly cloudy",
                    3: "Overcast",
                    45: "Foggy",
                    48: "Depositing rime fog",
                    51: "Light drizzle",
                    53: "Moderate drizzle",
                    55: "Dense drizzle",
                    61: "Slight rain",
                    63: "Moderate rain",
                    65: "Heavy rain",
                    71: "Slight snow",
                    73: "Moderate snow",
                    75: "Heavy snow",
                    77: "Snow grains",
                    80: "Slight rain showers",
                    81: "Moderate rain showers",
                    82: "Violent rain showers",
                    85: "Slight snow showers",
                    86: "Heavy snow showers",
                    95: "Thunderstorm",
                    96: "Thunderstorm with slight hail",
                    99: "Thunderstorm with heavy hail"
                }
                
                return {
                    'city': location['name'],
                    'country': location.get('country', 'Unknown'),
                    'temperature': current['temperature_2m'],
                    'humidity': current['relative_humidity_2m'],
                    'wind_speed': current['wind_speed_10m'],
                    'description': weather_codes.get(current['weather_code'], "Unknown"),
                    'timestamp': current['time']
                }
            else:
                return {'error': f"Weather API Error {weather_response.status_code}"}
        else:
            return {'error': f"Geocoding API Error {geo_response.status_code}"}
    except Exception as e:
        return {'error': str(e)}

def main():
    parser = argparse.ArgumentParser(description="Weather API Collector (Unsecure) for Splunk")
    parser.add_argument('--city', default="Sydney", help='City to get weather for')

    args = parser.parse_args()
    logger = splunk_common.setup_logging()

    try:
        # Fetch weather data
        splunk_common.log_json(logger, 'INFO', f"Fetching weather data for {args.city}")
        weather_data = get_weather_data(args.city)
        
        # Log the weather data
        splunk_common.log_json(
            logger,
            'INFO',
            weather_data,
            status='success' if 'error' not in weather_data else 'failure'
        )

    except Exception as e:
        splunk_common.log_json(logger, 'ERROR', f"Failed to get weather data: {str(e)}", status='failure')
        sys.exit(1)

if __name__ == '__main__':
    main()
