#!/usr/bin/env python3

import argparse
import json
import sys
import splunk_common
from splunk_secrets import SplunkSecrets

def store_credentials(realm, username, password, logger):
    """Store credentials in Splunk"""
    try:
        # Initialize SplunkSecrets
        secrets = SplunkSecrets(logger)
        
        # Store the credential
        result = secrets.store_credential(realm, username, password)
        
        if result:
            return {
                'realm': realm,
                'username': username,
                'action': 'store',
                'success': True,
                'message': 'Credential stored successfully'
            }
        else:
            return {'error': 'Failed to store credential'}
        
    except Exception as e:
        return {'error': str(e)}

def main():
    parser = argparse.ArgumentParser(description="Store Credentials in Splunk")
    parser.add_argument('--realm', required=True, help='Credential realm')
    parser.add_argument('--username', required=True, help='Credential username')
    parser.add_argument('--password', required=True, help='Password to store')

    args = parser.parse_args()
    logger = splunk_common.setup_logging()

    try:
        # Store credentials
        result = store_credentials(args.realm, args.username, args.password, logger)
        
        # Log success/failure to Splunk's internal logs
        if 'error' in result:
            splunk_common.log_json(logger, 'error', f"Failed to store credentials: {result['error']}", status='failure')
        else:
            splunk_common.log_json(logger, 'info', f"Successfully stored credentials for realm: {args.realm}, username: {args.username}", status='success')
        
        # Output the result to stdout
        print(json.dumps(result), flush=True)
        sys.stdout.flush()

    except Exception as e:
        error_msg = f"Failed to store credentials: {str(e)}"
        splunk_common.log_json(logger, 'error', error_msg, status='failure')
        print(json.dumps({'error': error_msg}), flush=True)
        sys.stdout.flush()
        sys.exit(1)

if __name__ == '__main__':
    main()