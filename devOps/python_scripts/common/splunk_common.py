import os
import json
import logging
import requests
import pathlib
from datetime import datetime

# Paths
current_file = pathlib.Path(__file__).resolve()
BASE_DIR = current_file.parents[5]
CERT_PATH = current_file.parent / 'splunk-8089.crt'

# JSON log formatter
class JsonFormatter(logging.Formatter):
    def format(self, record):
        log_record = {
            'ts': datetime.utcnow().isoformat() + 'Z',
            'level': record.levelname,
            'module': record.name,
            'message': record.getMessage(),
            'status': getattr(record, 'status', 'success')
        }
        return json.dumps(log_record)

def setup_logging(level):
    handler = logging.StreamHandler()
    handler.setFormatter(JsonFormatter())
    logger = logging.getLogger()
    logger.setLevel(level)
    logger.handlers = [handler]
    return logger

# Unified logger call with status
def log_json(logger, level, message, status='success'):
    log_func = getattr(logger, level.lower(), logger.info)
    log_func(message, extra={"status": status})

def load_app_config():
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

# Main wrapper for Splunk HTTP requests
def splunk_request(method, url, headers, data=None, verify=True):
    try:
        if method == 'GET':
            return requests.get(url, headers=headers, verify=verify)
        elif method == 'POST':
            return requests.post(url, headers=headers, data=data, verify=verify)
        elif method == 'DELETE':
            return requests.delete(url, headers=headers, verify=verify)
    except requests.exceptions.SSLError as ssl_err:
        raise RuntimeError(f"SSL verification failed: {ssl_err}")

# ----------- COMMON CLI HELPERS BELOW -----------

def add_common_args(parser):
    parser.add_argument('--app', required=True, help='Splunk app context')
    parser.add_argument('--dry-run', action='store_true', help='Simulate actions without making changes')
    parser.add_argument('--log-level', default='INFO', choices=['DEBUG', 'INFO', 'WARNING', 'ERROR'], help='Set logging level')
    parser.add_argument('--token', required=True, help='Splunk token')
    parser.add_argument('--base-url', required=True, help='Splunk base URL (e.g., https://splunk.local:8089)')
    parser.add_argument('--use-cert', action='store_true', help='Use local .crt file to verify Splunk server')

def extract_common_args(args):
    return args.app, args.dry_run, args.log_level.upper(), args.token, args.base_url

def init_logger(log_level):
    return setup_logging(getattr(logging, log_level))
