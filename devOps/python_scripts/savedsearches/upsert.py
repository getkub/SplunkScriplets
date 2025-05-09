import configparser
import requests
import json
import os
import sys
import argparse
import urllib3

# ────────────────────────────────
# Argument parsing
# ────────────────────────────────
parser = argparse.ArgumentParser(description="Upsert Splunk saved searches from .conf file")
parser.add_argument('--dry-run', action='store_true', default=True, help='Print actions without performing them (default: true)')
parser.add_argument('--real-run', dest='dry_run', action='store_false', help='Actually perform API requests (overrides dry-run)')
args = parser.parse_args()

# ────────────────────────────────
# Paths
# ────────────────────────────────
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONF_PATH = os.path.join(BASE_DIR, 'files', 'savedsearches.conf')
SETTINGS_PATH = os.path.join(BASE_DIR, '.vscode', 'settings.json')
CONFIG_PATH = os.path.join(BASE_DIR, 'files', 'config.json')
CERT_PATH = os.path.join(BASE_DIR, 'files', 'splunk-8089.crt')  # optional

# ────────────────────────────────
# Load token and baseUrl from settings.json
# ────────────────────────────────
try:
    with open(SETTINGS_PATH) as f:
        settings = json.load(f)['rest-client.environmentVariables']['$shared']
        token = settings['token']
except Exception as e:
    print("❌ Failed to load token or baseUrl:", e)
    sys.exit(1)

# ────────────────────────────────
# Load Splunk config
# ────────────────────────────────
try:
    with open(CONFIG_PATH) as f:
        config = json.load(f)
        app = config['app']
        owner = config['owner']
        baseUrl = config['baseUrl']
except Exception as e:
    print("❌ Failed to load config.json:", e)
    sys.exit(1)

# ────────────────────────────────
# Load savedsearches.conf
# ────────────────────────────────
parser_conf = configparser.ConfigParser()
parser_conf.read(CONF_PATH)

headers = {
    'Authorization': f'Bearer {token}',
    'Content-Type': 'application/x-www-form-urlencoded'
}

# Determine SSL cert verification method
verify_cert = CERT_PATH if os.path.exists(CERT_PATH) else False

if not verify_cert:
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    print("⚠️  WARNING: SSL verification is disabled. Using verify=False.\n")

mode = "DRY-RUN" if args.dry_run else "REAL RUN"
print(f"\n🧪 Starting {mode} for saved searches upload...\n")

# ────────────────────────────────
# Process each stanza in savedsearches.conf
# ────────────────────────────────
for stanza in parser_conf.sections():
    data = parser_conf[stanza]

    payload = {
        'name': stanza,
        'search': data.get('search'),
        'description': data.get('description', ''),
        'disabled': data.get('disabled', '0'),
        'is_scheduled': data.get('is_scheduled', '0'),
        'cron_schedule': data.get('cron_schedule', ''),
        'dispatch.earliest_time': data.get('dispatch.earliest_time', ''),
        'dispatch.latest_time': data.get('dispatch.latest_time', ''),
    }

    # Remove empty fields
    payload = {k: v for k, v in payload.items() if v}

    url = f"{baseUrl}/servicesNS/{owner}/{app}/saved/searches/{stanza}"
    check = requests.get(url, headers=headers, verify=verify_cert)

    if check.status_code == 200:
        print(f"🔄 {'Would update' if args.dry_run else 'Updating'} existing saved search: {stanza}")
        print(f"  → Endpoint: {url}")
        if not args.dry_run:
            r = requests.post(url, headers=headers, data=payload, verify=verify_cert)
    else:
        create_url = f"{baseUrl}/servicesNS/{owner}/{app}/saved/searches"
        print(f"➕ {'Would create' if args.dry_run else 'Creating'} new saved search: {stanza}")
        print(f"  → Endpoint: {create_url}")
        if not args.dry_run:
            r = requests.post(create_url, headers=headers, data=payload, verify=verify_cert)

    print("  → Payload:")
    for k, v in payload.items():
        print(f"     {k}: {v}")

    if args.dry_run:
        print("  🚫 Skipping actual POST (dry-run mode)\n")
    else:
        print(f"  ✅ Result: {r.status_code} {r.reason}\n")
