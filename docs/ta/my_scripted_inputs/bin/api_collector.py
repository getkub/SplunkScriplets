import requests
from common.splunk_secrets import get_splunk_credential

# App-specific constants
APP_NAME = "my_scripted_inputs"
USERNAME = "api_user"
REALM = "https://api.example.com"
API_ENDPOINT = "https://api.example.com/data"

# Step 1: Get API key from secure store
api_key = get_splunk_credential(APP_NAME, REALM, USERNAME)

# Step 2: Use it to call the external API
headers = {
    "Authorization": f"Bearer {api_key}"
}

try:
    response = requests.get(API_ENDPOINT, headers=headers)
    if response.status_code == 200:
        print(response.text)
    else:
        print(f"API call failed: {response.status_code} - {response.text}")
except Exception as e:
    print(f"API request error: {e}")
