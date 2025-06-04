import argparse
import requests
from common.splunk_secrets import get_splunk_credential

def main():
    parser = argparse.ArgumentParser(description="Splunk API Collector with secure credential access")
    parser.add_argument("--app", required=True, help="Splunk app name")
    parser.add_argument("--user", required=True, help="Username in Splunk's password store")
    parser.add_argument("--realm", required=True, help="Realm for credential (usually API base URL)")
    parser.add_argument("--endpoint", required=True, help="Full external API endpoint to call")

    args = parser.parse_args()

    # Step 1: Fetch stored password
    api_key = get_splunk_credential(app_name=args.app, realm=args.realm, username=args.user)

    # Step 2: Use the credential
    headers = {
        "Authorization": f"Bearer {api_key}"
    }

    try:
        response = requests.get(args.endpoint, headers=headers)
        if response.status_code == 200:
            print(response.text)  # Data to index
        else:
            print(f"API call failed: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"API request error: {e}")


if __name__ == "__main__":
    main()
