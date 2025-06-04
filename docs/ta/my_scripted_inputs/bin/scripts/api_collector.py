import requests
import json
import sys
import logging
from datetime import datetime
import os

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('/tmp/api_collector.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger('api_collector')

def get_splunk_credentials():
    try:
        # Get credentials from Splunk's environment
        api_key = os.environ.get('SPLUNK_API_KEY')
        api_url = os.environ.get('SPLUNK_API_URL')
        
        if not api_key or not api_url:
            raise Exception("API credentials not found in environment")
            
        return {
            'api_key': api_key,
            'api_url': api_url
        }
            
    except Exception as e:
        logger.error(f"Failed to get credentials: {str(e)}")
        sys.exit(1)

def make_api_call():
    try:
        # Get credentials from Splunk
        credentials = get_splunk_credentials()
        
        headers = {
            "Authorization": f"Bearer {credentials['api_key']}",
            "Content-Type": "application/json"
        }
        
        response = requests.get(credentials['api_url'], headers=headers)
        response.raise_for_status()
        
        data = response.json()
        
        # Add timestamp to each record
        timestamp = datetime.utcnow().isoformat()
        for record in data:
            record['_time'] = timestamp
            print(json.dumps(record))
            
    except requests.exceptions.RequestException as e:
        logger.error(f"API request failed: {str(e)}")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    make_api_call() 