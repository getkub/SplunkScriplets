#!/usr/bin/env python3

import os
import sys
import argparse
from getpass import getpass

# Import your common modules
from common import splunk_common
from common.splunk_secrets import SplunkSecrets

# Add splunklib to Python path
script_dir = os.path.dirname(os.path.abspath(__file__))
bin_dir = os.path.dirname(script_dir)
splunklib_path = os.path.join(bin_dir, 'splunklib')
sys.path.append(splunklib_path)

from splunklib import client
from splunklib.binding import HTTPError

class CredentialManager:
    def __init__(self, logger=None, splunk_username=None, splunk_password=None, app_context='search'):
        """Initialize CredentialManager with logging and Splunk connection details"""
        self.logger = logger or splunk_common.setup_logging()
        self.app_context = app_context
        
        # Use SplunkSecrets configuration for host/port
        secrets = SplunkSecrets(self.logger)
        self.splunk_host = secrets.splunkd_host
        self.splunk_port = secrets.splunkd_port
        
        # Store credentials for service connection
        self.splunk_username = splunk_username
        self.splunk_password = splunk_password
        
        splunk_common.log_json(self.logger, 'INFO', 'CredentialManager initialized', {
            'host': self.splunk_host,
            'port': self.splunk_port,
            'app_context': self.app_context
        })

    def _get_service(self):
        """Create and return Splunk service connection"""
        try:
            service = client.Service(
                host=self.splunk_host,
                port=self.splunk_port,
                username=self.splunk_username,
                password=self.splunk_password,
                app=self.app_context
            )
            
            splunk_common.log_json(self.logger, 'INFO', 'Successfully connected to Splunk service', {
                'host': self.splunk_host,
                'port': self.splunk_port
            })
            
            return service
            
        except Exception as e:
            splunk_common.log_json(self.logger, 'ERROR', f'Failed to connect to Splunk service: {str(e)}', {
                'host': self.splunk_host,
                'port': self.splunk_port,
                'error': str(e)
            })
            raise

    def add_credential(self, realm, username, credential_password):
        """Add a credential to Splunk's password storage"""
        
        credential_name = f"{realm}:{username}"
        
        try:
            service = self._get_service()
            storage_passwords = service.storage_passwords
            
            splunk_common.log_json(self.logger, 'INFO', f'Adding credential to Splunk', {
                'credential_name': credential_name,
                'realm': realm,
                'username': username,
                'app_context': self.app_context
            })
            
            # Add the credential
            storage_passwords.create(
                name=credential_name,
                password=credential_password,
                realm=realm
            )
            
            splunk_common.log_json(self.logger, 'INFO', 'Successfully added credential', {
                'credential_name': credential_name,
                'realm': realm,
                'username': username,
                'app_context': self.app_context
            })
            
            print(f"✅ Successfully added credential: {credential_name}")
            print(f"   Realm: {realm}")
            print(f"   Username: {username}")
            print(f"   App context: {self.app_context}")
            
            return True
            
        except HTTPError as e:
            if "already exists" in str(e):
                splunk_common.log_json(self.logger, 'WARNING', f'Credential already exists', {
                    'credential_name': credential_name,
                    'realm': realm,
                    'username': username,
                    'error': str(e)
                })
                print(f"⚠️  Credential {credential_name} already exists!")
                print("   Use update command to update existing credentials")
                return False
            else:
                splunk_common.log_json(self.logger, 'ERROR', f'HTTP error adding credential', {
                    'credential_name': credential_name,
                    'realm': realm,
                    'username': username,
                    'error': str(e)
                })
                print(f"❌ HTTP Error: {e}")
                return False
                
        except Exception as e:
            splunk_common.log_json(self.logger, 'ERROR', f'Unexpected error adding credential', {
                'credential_name': credential_name,
                'realm': realm,
                'username': username,
                'error': str(e)
            })
            print(f"❌ Error adding credential: {e}")
            return False

    def update_credential(self, realm, username, credential_password):
        """Update an existing credential in Splunk's password storage"""
        
        credential_name = f"{realm}:{username}"
        
        try:
            service = self._get_service()
            storage_passwords = service.storage_passwords
            
            splunk_common.log_json(self.logger, 'INFO', f'Updating credential in Splunk', {
                'credential_name': credential_name,
                'realm': realm,
                'username': username,
                'app_context': self.app_context
            })
            
            # Find and update the credential
            for credential in storage_passwords:
                if credential['realm'] == realm and credential['username'] == username:
                    credential.update(password=credential_password)
                    
                    splunk_common.log_json(self.logger, 'INFO', 'Successfully updated credential', {
                        'credential_name': credential_name,
                        'realm': realm,
                        'username': username,
                        'app_context': self.app_context
                    })
                    
                    print(f"✅ Successfully updated credential: {credential_name}")
                    return True
            
            # Credential not found
            splunk_common.log_json(self.logger, 'ERROR', f'Credential not found for update', {
                'credential_name': credential_name,
                'realm': realm,
                'username': username
            })
            print(f"❌ Credential not found: {credential_name}")
            print("   Use add command to create new credentials")
            return False
            
        except Exception as e:
            splunk_common.log_json(self.logger, 'ERROR', f'Error updating credential', {
                'credential_name': credential_name,
                'realm': realm,
                'username': username,
                'error': str(e)
            })
            print(f"❌ Error updating credential: {e}")
            return False

    def list_credentials(self):
        """List all stored credentials"""
        
        try:
            service = self._get_service()
            storage_passwords = service.storage_passwords
            
            splunk_common.log_json(self.logger, 'INFO', 'Listing stored credentials', {
                'app_context': self.app_context
            })
            
            credentials_list = []
            
            print("📋 Stored Credentials:")
            print("-" * 50)
            
            for credential in storage_passwords:
                cred_info = {
                    'realm': credential['realm'],
                    'username': credential['username'],
                    'app': credential.get('eai:acl', {}).get('app', 'N/A')
                }
                credentials_list.append(cred_info)
                
                print(f"Realm: {cred_info['realm']}")
                print(f"Username: {cred_info['username']}")
                print(f"App: {cred_info['app']}")
                print("-" * 30)
            
            splunk_common.log_json(self.logger, 'INFO', f'Successfully listed {len(credentials_list)} credentials', {
                'credentials_count': len(credentials_list),
                'app_context': self.app_context
            })
            
            return credentials_list
            
        except Exception as e:
            splunk_common.log_json(self.logger, 'ERROR', f'Error listing credentials', {
                'error': str(e),
                'app_context': self.app_context
            })
            print(f"❌ Error listing credentials: {e}")
            return []

    def verify_credential(self, realm, username):
        """Verify that a credential exists and can be retrieved"""
        
        credential_name = f"{realm}:{username}"
        
        try:
            # Use the existing SplunkSecrets class to test retrieval
            secrets = SplunkSecrets(self.logger)
            
            splunk_common.log_json(self.logger, 'INFO', f'Verifying credential retrieval', {
                'credential_name': credential_name,
                'realm': realm,
                'username': username
            })
            
            # This will test the actual retrieval mechanism your scripts use
            retrieved_password = secrets.get_credential(realm, username)
            
            if retrieved_password:
                splunk_common.log_json(self.logger, 'INFO', 'Credential verification successful', {
                    'credential_name': credential_name,
                    'realm': realm,
                    'username': username
                })
                print(f"✅ Credential verification successful: {credential_name}")
                print(f"   Password length: {len(retrieved_password)} characters")
                return True
            else:
                splunk_common.log_json(self.logger, 'ERROR', 'Credential verification failed - not found', {
                    'credential_name': credential_name,
                    'realm': realm,
                    'username': username
                })
                print(f"❌ Credential verification failed: {credential_name} not found")
                return False
                
        except Exception as e:
            splunk_common.log_json(self.logger, 'ERROR', f'Error verifying credential', {
                'credential_name': credential_name,
                'realm': realm,
                'username': username,
                'error': str(e)
            })
            print(f"❌ Error verifying credential: {e}")
            return False

def main():
    parser = argparse.ArgumentParser(description="Manage Splunk stored credentials using your existing modules")
    parser.add_argument("--splunk-user", default="admin", help="Splunk username (default: admin)")
    parser.add_argument("--app", default="search", help="App context (default: search)")
    parser.add_argument("--log-level", default="INFO", choices=['DEBUG', 'INFO', 'WARNING', 'ERROR'], 
                       help="Logging level (default: INFO)")
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Add credential command
    add_parser = subparsers.add_parser('add', help='Add a new credential')
    add_parser.add_argument("--realm", required=True, help="Credential realm")
    add_parser.add_argument("--username", required=True, help="Credential username")
    add_parser.add_argument("--password", help="Credential password (will prompt if not provided)")
    
    # Update credential command
    update_parser = subparsers.add_parser('update', help='Update existing credential')
    update_parser.add_argument("--realm", required=True, help="Credential realm")
    update_parser.add_argument("--username", required=True, help="Credential username")
    update_parser.add_argument("--password", help="New credential password (will prompt if not provided)")
    
    # List credentials command
    subparsers.add_parser('list', help='List all stored credentials')
    
    # Verify credential command
    verify_parser = subparsers.add_parser('verify', help='Verify credential can be retrieved')
    verify_parser.add_argument("--realm", required=True, help="Credential realm")
    verify_parser.add_argument("--username", required=True, help="Credential username")
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return

    # Set up logging with specified level
    log_level = getattr(splunk_common.logging, args.log_level)
    logger = splunk_common.setup_logging(log_level)
    
    splunk_common.log_json(logger, 'INFO', f'Starting credential management operation', {
        'command': args.command,
        'app_context': args.app,
        'splunk_user': args.splunk_user
    })
    
    # Get Splunk password
    splunk_password = getpass(f"Enter Splunk password for {args.splunk_user}: ")
    
    # Initialize credential manager
    try:
        cred_manager = CredentialManager(
            logger=logger,
            splunk_username=args.splunk_user,
            splunk_password=splunk_password,
            app_context=args.app
        )
    except Exception as e:
        splunk_common.log_json(logger, 'ERROR', f'Failed to initialize credential manager: {str(e)}')
        print(f"❌ Failed to initialize: {e}")
        sys.exit(1)
    
    # Execute the requested command
    success = False
    
    if args.command == 'add':
        credential_password = args.password or getpass("Enter credential password: ")
        success = cred_manager.add_credential(args.realm, args.username, credential_password)
    
    elif args.command == 'update':
        credential_password = args.password or getpass("Enter new credential password: ")
        success = cred_manager.update_credential(args.realm, args.username, credential_password)
    
    elif args.command == 'list':
        credentials = cred_manager.list_credentials()
        success = len(credentials) >= 0  # List operation is successful if it doesn't error
    
    elif args.command == 'verify':
        success = cred_manager.verify_credential(args.realm, args.username)
    
    # Log final status
    splunk_common.log_json(logger, 'INFO' if success else 'ERROR', 
                          f'Credential management operation completed', {
        'command': args.command,
        'success': success,
        'app_context': args.app
    })
    
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()