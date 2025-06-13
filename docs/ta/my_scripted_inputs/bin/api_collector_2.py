#!/usr/bin/env python3

import argparse
import requests
import sys
import os
from datetime import datetime, timedelta
from common import splunk_common
from common.splunk_secrets import SplunkSecrets

def get_date_range(days_back=1):
    """Get date range for API query"""
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days_back)
    return start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d')

def main():
    parser = argparse.ArgumentParser(description="Secure API Collector 2 for Splunk - Time Series Data")
    parser.add_argument('--url', required=True, help='API URL to fetch')
    parser.add_argument('--realm', required=True, help='Credential realm')
    parser.add_argument('--username', required=True, help='Credential username')
    parser.add_argument('--days', type=int, default=1, help='Number of days to look back')

    args = parser.parse_args()
    logger = splunk_common.setup_logging()
    secrets = SplunkSecrets(logger)

    try:
        # Get credentials from Splunk
        api_key = secrets.get_credential(args.realm, args.username)
        if not api_key:
            splunk_common.log_json(logger, 'ERROR', f"No credentials found for realm={args.realm}, username={args.username}", status='failure')
            sys.exit(1)

        # Get date range for query
        start_date, end_date = get_date_range(args.days)
        
        # Prepare API request
        headers = {
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json'
        }
        
        params = {
            'start_date': start_date,
            'end_date': end_date
        }
        
        splunk_common.log_json(logger, 'INFO', f"Fetching time series data from {args.url} for period {start_date} to {end_date}")
        
        # Make API request with credentials and parameters
        response = requests.get(
            args.url,
            headers=headers,
            params=params,
            timeout=30  # Longer timeout for time series data
        )
        
        if response.status_code == 200:
            data = response.json()
            
            # Process time series data
            for entry in data.get('time_series', []):
                # Log each time series entry
                splunk_common.log_json(
                    logger,
                    'INFO',
                    f"Time series entry: {entry}",
                    status='success'
                )
        else:
            splunk_common.log_json(logger, 'ERROR', f"API error {response.status_code}: {response.text}", status='failure')

    except Exception as e:
        splunk_common.log_json(logger, 'ERROR', f"Failed to query API: {str(e)}", status='failure')
        sys.exit(1)

if __name__ == '__main__':
    main() 