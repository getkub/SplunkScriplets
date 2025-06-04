import os
import requests
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def get_splunk_credential(app_name, realm, username, splunk_host="https://localhost:8089"):
    """
    Fetches a stored password from Splunk's credential store.
    
    Args:
        app_name: The name of your app (e.g., "my_scripted_inputs")
        realm: The realm used when storing the credential (e.g., "https://api.example.com")
        username: The stored username (e.g., "api_user")
        splunk_host: Usually https://localhost:8089
    
    Returns:
        clear_password: The decrypted password
    """
    session_token = os.environ.get('SPLUNKD_SESSION_KEY')
    if not session_token:
        raise Exception("Missing SPLUNKD_SESSION_KEY. Ensure 'passAuth = splunk-system-user' is set in inputs.conf.")

    headers = {
        'Authorization': f'Splunk {session_token}'
    }

    path = f"/servicesNS/nobody/{app_name}/storage/passwords/{realm}:{username}?output_mode=json"
    url = splunk_host + path

    response = requests.get(url, headers=headers, verify=False)

    if response.status_code != 200:
        raise Exception(f"Failed to retrieve credential: {response.status_code} - {response.text}")

    return response.json()['entry'][0]['content']['clear_password']
