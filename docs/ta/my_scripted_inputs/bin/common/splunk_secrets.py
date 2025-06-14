#!/usr/bin/env python3

import os
import sys
from . import splunk_common

# Add splunklib to Python path
script_dir = os.path.dirname(os.path.abspath(__file__))
bin_dir = os.path.dirname(script_dir)
splunklib_path = os.path.join(bin_dir, 'splunklib')
sys.path.append(splunklib_path)

from splunklib import client
from splunklib.binding import HTTPError

class SplunkSecrets:
    def __init__(self, logger=None):
        """Initialize SplunkSecrets with optional logger"""
        self.logger = logger or splunk_common.setup_logging()
        self.splunkd_port = os.environ.get('SPLUNK_MGMT_PORT', '8089')
        self.splunkd_host = os.environ.get('SPLUNK_MGMT_HOST', 'localhost')
        self._session_key = None  # To cache after reading

        # Debug: Log all environment variables (sanitized)
        env_log = {k: ("<hidden>" if "KEY" in k or "PASS" in k else v) for k, v in os.environ.items()}
        splunk_common.log_json(self.logger, 'debug', f"Environment variables: {env_log}")

    def get_session_key(self):
        """Get Splunk session key from stdin (passAuth context)"""
        if self._session_key:
            return self._session_key

        try:
            self.logger.debug("Attempting to read session key from stdin...")
            self._session_key = sys.stdin.readline().strip()

            if not self._session_key:
                raise ValueError("No session key found in stdin")

            splunk_common.log_json(self.logger, 'debug', f"Session key obtained from stdin: {bool(self._session_key)}")
            return self._session_key
        except Exception as e:
            splunk_common.log_json(self.logger, 'error', f"Failed to read session key from stdin: {str(e)}")
            raise

    def get_credential(self, realm, username):
        """Retrieve a specific credential from Splunk's storage using splunklib"""
        try:
            session_key = self.get_session_key()

            # Create a Splunk service instance
            service = client.Service(
                host=self.splunkd_host,
                port=self.splunkd_port,
                scheme='https',
                token=session_key
            )

            splunk_common.log_json(self.logger, 'info', f"Fetching credential for realm={realm}, username={username}")

            try:
                # Get the storage passwords collection
                storage_passwords = service.storage_passwords

                # Search for the specific credential
                for credential in storage_passwords:
                    if credential['realm'] == realm and credential['username'] == username:
                        splunk_common.log_json(self.logger, 'info', "Credential found successfully")
                        return credential['clear_password']

                splunk_common.log_json(self.logger, 'error', f"No credential found for realm={realm}, username={username}")
                return None

            except HTTPError as e:
                raise Exception(f"HTTP error while accessing credentials: {str(e)}")

        except Exception as e:
            splunk_common.log_json(self.logger, 'error', f"Failed to retrieve credential: {str(e)}")
            raise
