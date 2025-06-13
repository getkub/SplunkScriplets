#!/usr/bin/env python3

import argparse
import json
import sys
import splunk_common
from splunk_secrets import SplunkSecrets

def check_credentials(realm, username, logger):
    """Check if credentials can be retrieved from Splunk"""
    try:
        # Initialize SplunkSecrets
        secrets = SplunkSecrets(logger)
        
        # Get the credential
        password = secrets.get_credential(realm, username)
        
        if not password:
            return {'error': f"No credentials found for realm '{realm}' and username '{username}'"}
        
        return {
            'realm': realm,
            'username': username,
            'credentials_found': True,
            'password': password
        }
        
    except Exception as e:
        return {'error': str(e)}

def main():
    parser = argparse.ArgumentParser(description="Credential Checker for Splunk")
    parser.add_argument('--realm', required=True, help='Credential realm')
    parser.add_argument('--username', required=True, help='Credential username')

    args = parser.parse_args()
    logger = splunk_common.setup_logging()

    try:
        # Check credentials
        result = check_credentials(args.realm, args.username, logger)
        
        # Log success/failure to Splunk's internal logs
        if 'error' in result:
            splunk_common.log_json(logger, 'error', f"Failed to retrieve credentials: {result['error']}", status='failure')
        else:
            splunk_common.log_json(logger, 'info', f"Successfully retrieved credentials for realm: {args.realm}, username: {args.username}", status='success')
        
        # Output the result to stdout for Splunk indexing
        print(json.dumps(result), flush=True)
        sys.stdout.flush()

    except Exception as e:
        error_msg = f"Failed to check credentials: {str(e)}"
        splunk_common.log_json(logger, 'error', error_msg, status='failure')
        print(json.dumps({'error': error_msg}), flush=True)
        sys.stdout.flush()
        sys.exit(1)

if __name__ == '__main__':
    main()