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
parser_args = argparse.ArgumentParser(description="Upsert saved searches to Splunk.")
parser_args.add_argument('--dry-run', dest='dry_run', action='store_true', default=True, help='Perform a dry run (default)')
parser_args.add_argument('--insert', dest='dry_run', action='store_false', help='Actually perform the insertion')
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

log.info("Starting %s saved search sync...\n", "DRY-RUN" if args.dry_run else "ACTUAL")

for stanza in conf_parser.sections():
    data = conf_parser[stanza]

    # Convert all items in the stanza to a dictionary
    payload = {k: v for k, v in data.items() if v.strip() != ""}

    # Ensure name is explicitly included
    payload['name'] = stanza

    url = f"{baseUrl}/servicesNS/{owner}/{app}/saved/searches/{stanza}"
    try:
        check = requests.get(url, headers=headers, verify=CERT_PATH)
    except requests.exceptions.SSLError as ssl_err:
        log.error("SSL verification failed for %s: %s", url, ssl_err)
        continue

    if check.status_code == 200:
        log.info("🔄 Existing saved search found: %s", stanza)
        if not args.dry_run:
            del_response = requests.delete(url, headers=headers, verify=CERT_PATH)
            if del_response.status_code >= 400:
                log.error("❌ Delete failed for %s: %s - %s", stanza, del_response.status_code, del_response.reason)
                log.debug("Response: %s", del_response.text)
                continue
            else:
                log.info("🗑️ Deleted existing saved search: %s", stanza)
    else:
        log.info("➕ No existing saved search. Will create: %s", stanza)

    if not args.dry_run:
        create_response = requests.post(
            f"{baseUrl}/servicesNS/{owner}/{app}/saved/searches",
            headers=headers,
            data=payload,
            verify=CERT_PATH
        )
        if create_response.status_code >= 400:
            log.error("❌ Create failed: %s - %s", create_response.status_code, create_response.reason)
            log.debug("Response: %s", create_response.text)
        else:
            log.info("✅ Created: %s", stanza)

    if args.log_level.upper() == "DEBUG":
        log.debug("→ Payload: %s", json.dumps(payload, indent=2))

    if args.dry_run:
        log.info("🚫 Skipping actual POST (dry-run mode)")

    print()
