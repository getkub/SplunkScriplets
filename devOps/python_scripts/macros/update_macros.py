#!/usr/bin/env python3

import requests
import json
import os
import sys
import argparse
import logging
import re

# Base paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SETTINGS_PATH = os.path.join(BASE_DIR, '.vscode', 'settings.json')
CONFIG_PATH = os.path.join(BASE_DIR, 'files', 'config.json')
CERT_PATH = os.path.join(BASE_DIR, 'files', 'splunk-8089.crt')

# Argument parsing
parser_args = argparse.ArgumentParser(description="Update or delete macros in Splunk.")
parser_args.add_argument('--action-flag', choices=['updateOnly', 'deleteOnly'], help='Perform update or delete')
parser_args.add_argument('--dry-run', action='store_true', default=True, help='Perform a dry run (default)')
parser_args.add_argument('--log-level', default='INFO', choices=['DEBUG', 'INFO', 'WARNING', 'ERROR'], help='Set log verbosity')
parser_args.add_argument('--conf-path', required=True, help='Path to the .conf file (e.g., files/cloudtrail.conf)')
args = parser_args.parse_args()

# Logging setup
logging.basicConfig(
    level=getattr(logging, args.log_level.upper()),
    format='%(levelname)s: %(message)s'
)
log = logging.getLogger()

# Validate conf path
CONF_PATH = os.path.join(BASE_DIR, args.conf_path)
if not os.path.exists(CONF_PATH):
    log.error("❌ Config file not found at path: %s", CONF_PATH)
    sys.exit(1)

# Load token and base URL from settings
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

# Parse Splunk .conf file
def parse_splunk_conf(file_path):
    conf_data = {}
    current_stanza = None
    key = None
    buffer = ""

    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.rstrip()
            if not line or line.strip().startswith('#'):
                continue
            if line.startswith('[') and line.endswith(']'):
                if key and buffer and current_stanza:
                    conf_data[current_stanza][key] = buffer.strip()
                    buffer = ""
                    key = None
                current_stanza = line[1:-1]
                conf_data[current_stanza] = {}
            elif '=' in line and current_stanza and not line.startswith(' '):
                if key and buffer:
                    conf_data[current_stanza][key] = buffer.strip()
                key, val = line.split('=', 1)
                key = key.strip()
                buffer = val.strip()
            elif current_stanza and key:
                buffer += '\n' + line.strip()

        if key and buffer and current_stanza:
            conf_data[current_stanza][key] = buffer.strip()

    return conf_data

# Load macro configuration
conf_data = parse_splunk_conf(CONF_PATH)

headers = {
    'Authorization': f'Bearer {token}',
    'Content-Type': 'application/x-www-form-urlencoded'
}

action_mode = args.action_flag.upper() if args.action_flag else "CHECK"
log.info("🔧 Mode: %s (%s)", action_mode, "DRY-RUN" if args.dry_run else "EXECUTE")

# Main macro loop
for stanza, data in conf_data.items():
    payload = {k: v for k, v in data.items() if v.strip() != ""}
    name = stanza
    url = f"{baseUrl}/servicesNS/{owner}/{app}/configs/conf-macros/{name}"

    try:
        check = requests.get(url, headers=headers, verify=CERT_PATH)
    except requests.exceptions.SSLError as ssl_err:
        log.error("SSL verification failed for %s: %s", url, ssl_err)
        continue

    exists = check.status_code == 200

    if args.action_flag == 'deleteOnly':
        if exists:
            log.info("🗑️ Macro Exists and will be deleted: %s", name)
            del_response = requests.delete(url, headers=headers, verify=CERT_PATH)
            if del_response.status_code >= 400:
                log.error("❌ Delete failed: %s - %s", del_response.status_code, del_response.reason)
            else:
                log.info("✅ Macro Deleted: %s", name)
        else:
            log.warning("❓ Not found: %s", name)

    elif args.action_flag == 'updateOnly':
        if exists:
            log.info("✏️ Updating existing macro: %s", name)
            response = requests.post(url, headers=headers, data=payload, verify=CERT_PATH)
            if response.status_code >= 400:
                log.error("❌ Update failed for %s: %s - %s", name, response.status_code, response.reason)
                log.debug("Response: %s", response.text)
            else:
                log.info("✅ Updated: %s", name)
        else:
            log.warning("📄 Not found: %s", name)
            payload['name'] = name
            create_url = f"{baseUrl}/servicesNS/{owner}/{app}/configs/conf-macros"
            response = requests.post(create_url, headers=headers, data=payload, verify=CERT_PATH)
            if response.status_code >= 400:
                log.error("❌ Create failed for %s: %s - %s", name, response.status_code, response.reason)
                log.debug("Response: %s", response.text)
            else:
                log.info("✅ Created: %s", name)

    else:
        if exists:
            log.info("✉️ Exists: %s", name)
        else:
            log.warning("❓ Not found: %s", name)

print()
