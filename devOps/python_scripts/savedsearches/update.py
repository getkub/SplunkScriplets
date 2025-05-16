import configparser
import requests
import json
import os
import sys
import argparse
import logging

# Base paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONF_PATH = os.path.join(BASE_DIR, 'files', 'savedsearches.conf')
SETTINGS_PATH = os.path.join(BASE_DIR, '.vscode', 'settings.json')
CONFIG_PATH = os.path.join(BASE_DIR, 'files', 'config.json')
CERT_PATH = os.path.join(BASE_DIR, 'files', 'splunk-8089.crt')

# argparse
parser_args = argparse.ArgumentParser(description="Update or delete saved searches in Splunk.")
parser_args.add_argument('--action-flag', choices=['updateOnly', 'deleteOnly'], help='Perform update or delete')
parser_args.add_argument('--dry-run', action='store_true', default=True, help='Perform a dry run (default)')
parser_args.add_argument('--log-level', default='INFO', choices=['DEBUG', 'INFO', 'WARNING', 'ERROR'], help='Set log verbosity')
args = parser_args.parse_args()

# Logging setup
logging.basicConfig(
    level=getattr(logging, args.log_level.upper()),
    format='%(levelname)s: %(message)s'
)
log = logging.getLogger()

# Load token and baseUrl
try:
    with open(SETTINGS_PATH) as f:
        settings = json.load(f)['rest-client.environmentVariables']['$shared']
        token = settings['token']
        baseUrl = settings['baseUrl']
except Exception as e:
    log.error("Failed to load token or baseUrl: %s", e)
    sys.exit(1)

# Load Splunk config
try:
    with open(CONFIG_PATH) as f:
        config = json.load(f)
        app = config['app']
        owner = config['owner']
except Exception as e:
    log.error("Failed to load config.json: %s", e)
    sys.exit(1)

# Load savedsearches.conf
conf_parser = configparser.RawConfigParser(strict=False, delimiters=('='))
conf_parser.optionxform = str  # preserve case sensitivity
conf_parser.read(CONF_PATH)

headers = {
    'Authorization': f'Bearer {token}',
    'Content-Type': 'application/x-www-form-urlencoded'
}

action_mode = args.action_flag.upper() if args.action_flag else "CHECK"
log.info("🔧 Mode: %s (%s)", action_mode, "DRY-RUN" if args.dry_run else "EXECUTE")

for stanza in conf_parser.sections():
    data = conf_parser[stanza]
    payload = {k: v for k, v in data.items() if v.strip() != ""}
    name = stanza

    url = f"{baseUrl}/servicesNS/{owner}/{app}/saved/searches/{name}"
    try:
        check = requests.get(url, headers=headers, verify=CERT_PATH)
    except requests.exceptions.SSLError as ssl_err:
        log.error("SSL verification failed for %s: %s", url, ssl_err)
        continue

    exists = check.status_code == 200

    if args.action_flag == 'deleteOnly':
        if exists:
            log.info("🗑️ Exists and will be deleted: %s", name)
            del_response = requests.delete(url, headers=headers, verify=CERT_PATH)
            if del_response.status_code >= 400:
                log.error("❌ Delete failed: %s - %s", del_response.status_code, del_response.reason)
            else:
                log.info("✅ Deleted: %s", name)
        else:
            log.warning("❓ Not found: %s", name)

    elif args.action_flag == 'updateOnly':
        if exists:
            log.info("✏️ Updating existing saved search: %s", name)
            update_url = f"{baseUrl}/servicesNS/{owner}/{app}/saved/searches/{name}"
            response = requests.post(update_url, headers=headers, data=payload, verify=CERT_PATH)
            if response.status_code >= 400:
                log.error("❌ Update failed for %s: %s - %s", name, response.status_code, response.reason)
                log.debug("Response: %s", response.text)
            else:
                log.info("✅ Updated: %s", name)
        else:
            log.warning("📬 Not found: %s", name)
            payload['name'] = name  # only include 'name' when creating
            create_url = f"{baseUrl}/servicesNS/{owner}/{app}/saved/searches"
            response = requests.post(create_url, headers=headers, data=payload, verify=CERT_PATH)
            if response.status_code >= 400:
                log.error("❌ Create failed for %s: %s - %s", name, response.status_code, response.reason)
                log.debug("Response: %s", response.text)
            else:
                log.info("✅ Created: %s", name)

    else:
        # Default: Just check
        if exists:
            log.info("✉️ Exists: %s", name)
        else:
            log.warning("❓ Not found: %s", name)

    print()
