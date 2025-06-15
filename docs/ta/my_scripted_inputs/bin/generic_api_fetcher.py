#!/usr/bin/env python3

import argparse
import requests
import json
import sys
from common import splunk_common
from common.splunk_secrets import SplunkSecrets

def fetch_api_data(api_url, api_key=None):
    headers = {}
    if api_key:
        headers['X-API-Key'] = api_key  # Set only this header

    try:
        response = requests.get(api_url, headers=headers, timeout=10)  # Pass headers here
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
    parser.add_argument("--realm", required=True, help="Splunk credential realm")
    parser.add_argument("--username", required=True, help="Splunk credential username")
    parser.add_argument("--source-name", default="generic_api", help="Source name for Splunk indexing (default: generic_api)")
    args = parser.parse_args()

    logger = splunk_common.setup_logging()
    
    try:
        secrets = SplunkSecrets(logger)
        api_key = secrets.get_credential(args.realm, args.username)
        
        if not api_key:
            splunk_common.log_json(logger, "ERROR", "Failed to retrieve API key from Splunk", {
                "realm": args.realm,
                "username": args.username
            })
            sys.exit(1)
            
        splunk_common.log_json(logger, "INFO", "Successfully retrieved API key from Splunk", {
            "realm": args.realm,
            "username": args.username
        })

    except Exception as e:
        splunk_common.log_json(logger, "ERROR", f"Failed to initialize Splunk secrets: {str(e)}", {
            "realm": args.realm,
            "username": args.username
        })
        sys.exit(1)
    print(f"DEBUG: API key from Splunk secrets: {api_key}", file=sys.stderr)
    data = fetch_api_data(args.api_url, api_key)

    if "error" in data:
        splunk_common.log_json(logger, "ERROR", f"API fetch failed", {
            "api_url": args.api_url,
            "realm": args.realm,
            "username": args.username,
            "error": data["error"]
        })
        sys.exit(1)

    splunk_common.log_json(logger, "INFO", "API fetch succeeded", {
        "api_url": args.api_url,
        "realm": args.realm,
        "username": args.username,
        "status_code": data.get("status_code")
    })

    output_data = {
        "timestamp": datetime.now(timezone(timedelta(hours=10))).isoformat(timespec='seconds'),
        "source": args.source_name,
        "api_url": args.api_url,
        "status_code": data["status_code"],
        "api_response_time": data["api_response_time"],
        "content_type": data["content_type"],
        "realm": args.realm,
        "username": args.username,
        "api_data": data["api_data"]
    }
    
    print(json.dumps(output_data), flush=True)

if __name__ == "__main__":
    main()
