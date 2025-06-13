#!/usr/bin/env python3

import argparse
import requests
from common import splunk_common

def main():
    parser = argparse.ArgumentParser(description="Fetch weather without secrets")
    parser.add_argument('--url', required=True, help='Weather API URL to fetch')

    args = parser.parse_args()
    logger = splunk_common.setup_logging()

    splunk_common.log_json(logger, 'INFO', f"Fetching weather data from {args.url}")

    try:
        response = requests.get(args.url, timeout=5)
        if response.status_code == 200:
            weather = response.text.strip()
            splunk_common.log_json(logger, 'INFO', f"Weather result: {weather}")
        else:
            splunk_common.log_json(logger, 'ERROR', f"API error {response.status_code}: {response.text}", status='failure')

    except Exception as e:
        splunk_common.log_json(logger, 'ERROR', f"Failed to query weather API: {e}", status='failure')

if __name__ == '__main__':
    main()
