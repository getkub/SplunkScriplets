import os
import json
import logging
import requests
import pathlib

current_file = pathlib.Path(__file__).resolve()
BASE_DIR = current_file.parents[3]
# print("BASE_DIR:", BASE_DIR)

SETTINGS_PATH = os.path.join(BASE_DIR, 'settings.json')
CERT_PATH = current_file.parent / 'splunk-8089.crt'

def setup_logging(level):
    logging.basicConfig(level=level, format='%(levelname)s: %(message)s')
    return logging.getLogger()

def load_auth_settings():
    try:
        with open(SETTINGS_PATH) as f:
            settings = json.load(f)['rest-client.environmentVariables']['$shared']
            return settings['token'], settings['baseUrl']
    except Exception as e:
        raise RuntimeError(f"Failed to load token/baseUrl: {e}")

def load_app_config():
    # Hardcoded app name and owner
    return "app_name", "nobody"

def parse_splunk_conf(file_path):
    conf_data, current_stanza, key, buffer = {}, None, None, ""
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.rstrip()
            if not line or line.strip().startswith('#'):
                continue
            if line.startswith('[') and line.endswith(']'):
                if key and buffer and current_stanza:
                    conf_data[current_stanza][key] = buffer.strip()
                    buffer = ""
                current_stanza = line[1:-1]
                conf_data[current_stanza] = {}
                key = None
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

def splunk_request(method, url, headers, data=None):
    try:
        if method == 'GET':
            return requests.get(url, headers=headers, verify=CERT_PATH)
        elif method == 'POST':
            return requests.post(url, headers=headers, data=data, verify=CERT_PATH)
        elif method == 'DELETE':
            return requests.delete(url, headers=headers, verify=CERT_PATH)
    except requests.exceptions.SSLError as ssl_err:
        raise RuntimeError(f"SSL verification failed: {ssl_err}")

# ----------- NEW COMMON CLI HELPERS BELOW -----------

def add_common_args(parser):
    parser.add_argument('--app', required=True, help='Splunk app context')
    parser.add_argument('--dry-run', action='store_true', help='Simulate actions without making changes')
    parser.add_argument('--log-level', default='INFO', choices=['DEBUG', 'INFO', 'WARNING', 'ERROR'], help='Set logging level')

def extract_common_args(args):
    return args.app, args.dry_run, args.log_level.upper()

def init_logger(log_level):
    return setup_logging(getattr(logging, log_level))
