import logging
import json
import os
from datetime import datetime, timezone, timedelta

# Configuration variables
SPLUNK_HOME = os.environ.get('SPLUNK_HOME', '/opt/splunk')
SCRIPT_NAME = 'my_scripted_input'

class JsonFormatter(logging.Formatter):
    def format(self, record):
        log_record = {
            'ts': datetime.now(timezone(timedelta(hours=10))).isoformat(timespec='seconds'),
            'level': record.levelname,
            'module': record.name,
            'message': record.getMessage(),
            'status': getattr(record, 'status', 'success')
        }
        return json.dumps(log_record)

def setup_logging(level=logging.INFO):
    logfile = f'{SPLUNK_HOME}/var/log/splunk/{SCRIPT_NAME}.log'
    handler = logging.FileHandler(logfile)
    handler.setFormatter(JsonFormatter())
    logger = logging.getLogger()
    logger.setLevel(level)
    logger.handlers = [handler]
    return logger

def log_json(logger, level, message, status='success'):
    log_func = getattr(logger, level.lower(), logger.info)
    log_func(message, extra={"status": status})