#!/usr/bin/env python3

import os
import sys
import json
import argparse
from datetime import datetime

# Add common directory to Python path
script_dir = os.path.dirname(os.path.abspath(__file__))
bin_dir = os.path.dirname(script_dir)
common_dir = os.path.join(bin_dir, 'common')
sys.path.append(common_dir)

from common import splunk_common
from common.splunk_secrets import SplunkSecrets

class WeatherAlert:
    def __init__(self, logger=None):
        """Initialize WeatherAlert with optional logger"""
        self.logger = logger or splunk_common.setup_logging()
        self.secrets = SplunkSecrets(self.logger)

    def process_alert(self, alert_data):
        """Process alert data and take action"""
        try:
            # Log the alert data
            splunk_common.log_json(self.logger, 'info', f"Processing alert: {alert_data}")
            
            # Extract relevant information
            search_name = alert_data.get('search_name', 'Unknown Search')
            app = alert_data.get('app', 'Unknown App')
            owner = alert_data.get('owner', 'Unknown Owner')
            results_file = alert_data.get('results_file', '')
            
            # Read the results file
            if results_file and os.path.exists(results_file):
                with open(results_file, 'r') as f:
                    results = json.load(f)
                splunk_common.log_json(self.logger, 'info', f"Alert results: {results}")
            
            # Here you can add your custom alert action logic
            # For example, sending notifications, making API calls, etc.
            
            splunk_common.log_json(self.logger, 'info', "Alert processed successfully")
            return True
            
        except Exception as e:
            splunk_common.log_json(self.logger, 'error', f"Failed to process alert: {str(e)}")
            return False

def main():
    parser = argparse.ArgumentParser(description='Weather Alert Action')
    parser.add_argument('--alert_data', required=True, help='JSON string containing alert data')
    args = parser.parse_args()
    
    try:
        # Parse alert data
        alert_data = json.loads(args.alert_data)
        
        # Initialize and process alert
        alert = WeatherAlert()
        success = alert.process_alert(alert_data)
        
        if not success:
            sys.exit(1)
            
    except Exception as e:
        splunk_common.log_json(None, 'error', f"Alert action failed: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main() 