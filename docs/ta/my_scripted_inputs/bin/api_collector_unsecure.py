#!/usr/bin/env python3

import argparse
import requests
import sys
from common import splunk_common

def get_weather_data(city):
    """Fetch weather data from wttr.in API"""
    try:
        url = f"https://wttr.in/{city}?format=3"
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            return response.text.strip()
        else:
            raise Exception(f"API error {response.status_code}: {response.text}")
    except Exception as e:
        raise Exception(f"Failed to fetch weather data: {str(e)}")

def main():
    parser = argparse.ArgumentParser(description="Weather API Collector (Unsecure) for Splunk")
    parser.add_argument('--city', default="Melbourne", help='City to get weather for')

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
            f"Weather data for {args.city}: {weather_data}",
            status='success'
        )

    except Exception as e:
        splunk_common.log_json(logger, 'ERROR', f"Failed to get weather data: {str(e)}", status='failure')
        sys.exit(1)

if __name__ == '__main__':
    main()
