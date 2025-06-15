#!/usr/bin/env python3

import argparse
import requests
import json
import sys
from datetime import datetime, timezone
from common import splunk_common  # only for logging

def fetch_api_data(api_url, api_key):
    headers = {
        'X-API-Key': api_key
    }
    try:
        response = requests.get(api_url, headers=headers, timeout=10)
        if response.status_code != 200:
            return {"error": f"API request failed: {response.status_code} - {response.text}"}
        data = response.json()
        return {
            "api_data": data,
            "status_code": response.status_code,
            "api_response_time": response.elapsed.total_seconds(),
            "content_type": response.headers.get('content-type', 'unknown')
        }
    except Exception as e:
        return {"error": f"Unexpected error: {str(e)}"}

def main():
    parser = argparse.ArgumentParser(description="Fetch data from any API endpoint")
    parser.add_argument("--api-url", required=True, help="API endpoint URL to fetch data from")
    parser.add_argument("--source-name", default="generic_api", help="Source name for Splunk indexing (default: generic_api)")
    args = parser.parse_args()

    logger = splunk_common.setup_logging()

    # Hardcoded API key for testing only
    api_key = "reqres-free-v1"

    splunk_common.log_json(logger, "INFO", "Using hardcoded API key for testing")

    data = fetch_api_data(args.api_url, api_key)

    if "error" in data:
        splunk_common.log_json(logger, "ERROR", "API fetch failed", {
            "api_url": args.api_url,
            "error": data["error"]
        })
        sys.exit(1)

    splunk_common.log_json(logger, "INFO", "API fetch succeeded", {
        "api_url": args.api_url,
        "status_code": data.get("status_code")
    })

    # Generate ISO8601 timestamp inline, no splunk_common call
    timestamp = datetime.now(timezone.utc).isoformat(timespec='milliseconds')

    output_data = {
        "timestamp": timestamp,
        "source": args.source_name,
        "api_url": args.api_url,
        "status_code": data["status_code"],
        "api_response_time": data["api_response_time"],
        "content_type": data["content_type"],
        "api_data": data["api_data"]
    }

    print(json.dumps(output_data), flush=True)

if __name__ == "__main__":
    main()
