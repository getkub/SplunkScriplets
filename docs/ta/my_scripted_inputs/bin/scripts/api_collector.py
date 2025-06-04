#!/usr/bin/env python3

import requests
import json
import sys
import logging
from datetime import datetime

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

def make_api_call():
    try:
        # Replace with your actual API endpoint and authentication
        api_url = "https://api.example.com/data"
        headers = {
            "Authorization": "Bearer YOUR_API_TOKEN",
            "Content-Type": "application/json"
        }
        
        response = requests.get(api_url, headers=headers)
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