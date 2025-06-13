#!/usr/bin/env python3

import os
import requests
import splunk_common

class SplunkSecrets:
    def __init__(self, logger=None):
        """Initialize SplunkSecrets with optional logger"""
        self.logger = logger or splunk_common.setup_logging()
        self.splunkd_port = os.environ.get('SPLUNK_MGMT_PORT', '8089')
        self.splunkd_host = os.environ.get('SPLUNK_MGMT_HOST', 'localhost')

    def get_session_key(self):
        """Get Splunk session key from environment"""
        session_key = os.environ.get('SPLUNK_SESSION_KEY')
        if not session_key:
            raise ValueError("No session key found in environment")
        return session_key

    def get_credential(self, realm, username):
        """Retrieve a specific credential from Splunk's storage"""
        try:
            session_key = self.get_session_key()
            url = f"https://{self.splunkd_host}:{self.splunkd_port}/services/storage/passwords"
            
            headers = {
                'Authorization': f'Splunk {session_key}',
                'Content-Type': 'application/json'
            }
            
            splunk_common.log_json(self.logger, 'info', f"Fetching credential for realm={realm}, username={username}")
            
            response = requests.get(
                url,
                headers=headers,
                verify=False,  # Note: In production, you should properly handle SSL verification
                timeout=5
            )
            
            if response.status_code != 200:
                raise Exception(f"Failed to get credentials: {response.status_code} - {response.text}")
                
            data = response.json()
            for entry in data.get('entry', []):
                content = entry.get('content', {})
                if content.get('realm') == realm and content.get('username') == username:
                    splunk_common.log_json(self.logger, 'info', "Credential found successfully")
                    return content.get('clear_password')
                    
            splunk_common.log_json(self.logger, 'error', f"No credential found for realm={realm}, username={username}")
            return None
            
        except Exception as e:
            splunk_common.log_json(self.logger, 'error', f"Failed to retrieve credential: {str(e)}")
            raise

    def store_credential(self, realm, username, password):
        """Store a new credential in Splunk's storage"""
        try:
            session_key = self.get_session_key()
            url = f"https://{self.splunkd_host}:{self.splunkd_port}/services/storage/passwords"
            
            headers = {
                'Authorization': f'Splunk {session_key}',
                'Content-Type': 'application/x-www-form-urlencoded'
            }
            
            data = {
                'name': realm,
                'username': username,
                'password': password
            }
            
            splunk_common.log_json(self.logger, 'info', f"Storing credential for realm={realm}, username={username}")
            
            response = requests.post(
                url,
                headers=headers,
                data=data,
                verify=False,  # Note: In production, you should properly handle SSL verification
                timeout=5
            )
            
            if response.status_code not in (200, 201):
                raise Exception(f"Failed to store credential: {response.status_code} - {response.text}")
                
            splunk_common.log_json(self.logger, 'info', "Credential stored successfully")
            return True
            
        except Exception as e:
            splunk_common.log_json(self.logger, 'error', f"Failed to store credential: {str(e)}")
            raise