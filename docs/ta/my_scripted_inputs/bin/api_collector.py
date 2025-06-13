#!/usr/bin/env python3

import argparse
import requests
import sys
import os
from common import splunk_common
from common.splunk_secrets import SplunkSecrets

def main():
    parser = argparse.ArgumentParser(description="Secure API Collector for Splunk")
    parser.add_argument('--url', required=True, help='API URL to fetch')
    parser.add_argument('--realm', required=True, help='Credential realm')
    parser.add_argument('--username', required=True, help='Credential username')

    args = parser.parse_args()
    logger = splunk_common.setup_logging()
    secrets = SplunkSecrets(logger)

    try:
        # Get credentials from Splunk
        api_key = secrets.get_credential(args.realm, args.username)
        if not api_key:
            splunk_common.log_json(logger, 'ERROR', f"No credentials found for realm={args.realm}, username={args.username}", status='failure')
            sys.exit(1)

        # Make API request with credentials
        headers = {
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json'
        }
        
        splunk_common.log_json(logger, 'INFO', f"Fetching data from {args.url}")
        response = requests.get(args.url, headers=headers, timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            splunk_common.log_json(logger, 'INFO', f"API response: {data}")
        else:
            splunk_common.log_json(logger, 'ERROR', f"API error {response.status_code}: {response.text}", status='failure')

    except Exception as e:
        splunk_common.log_json(logger, 'ERROR', f"Failed to query API: {str(e)}", status='failure')
        sys.exit(1)

if __name__ == '__main__':
    main() 