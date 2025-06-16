#!/usr/bin/env python3

import argparse
import requests
import json
import sys
from common import splunk_common
from datetime import datetime, timezone

def fetch_api_data(api_url):
    try:
        response = requests.get(api_url, timeout=10)
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
    parser = argparse.ArgumentParser(description="Fetch data from a public API (no auth required)")
    parser.add_argument("--api-url", required=True, help="API endpoint URL to fetch data from")
    parser.add_argument("--source-name", default="generic_api", help="Source name for Splunk indexing (default: generic_api)")
    args = parser.parse_args()

    logger = splunk_common.setup_logging()

    splunk_common.log_json(logger, "INFO", "Starting API fetch", {
        "api_url": args.api_url
    })

    data = fetch_api_data(args.api_url)

    if "error" in data:
        splunk_common.log_json(logger, "ERROR", "API fetch failed", {
            "api_url": args.api_url,
            "error": data["error"]
        })
        sys.exit(1)

    splunk_common.log_json(logger, "INFO", "API fetch succeeded", {
        "api_url": args.api_url,
        "status_code": data["status_code"]
    })

    output_data = {
        "timestamp": datetime.now(timezone.utc).isoformat(timespec='seconds'),
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
