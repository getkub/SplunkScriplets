import sys
import os
import datetime
import logging
import logging.handlers

def setup_logger(level,module):
    logger = logging.getLogger(module)
    logger.propagate = False # Prevent the log messages from being duplicated in the python.log file
    logger.setLevel(level)
    file_handler = logging.handlers.RotatingFileHandler(os.environ['SPLUNK_HOME'] + '/var/log/splunk/' + 'df_' + module + '.log', maxBytes=25000000, backupCount=5)
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    return logger

# Setup the handler with defaults
thisModule="diaryfolio_Module"
logger = setup_logger(logging.INFO,thisModule)
runId = datetime.datetime.utcnow().strftime('%Y%m%d%H%M%S')

# Rest of the logic 
f = open ('/tmp/echo.txt', 'a')
f.write(datetime.datetime.now().strftime("%F %T") + ' ' + 'hello python' + str(sys.argv) + '\n')
status="Success"
msg_summary="echo"
msg_details='hello python' + str(sys.argv)
logger.info('runId=' + runId + ' status=' + status + ' msg_summary=' + msg_summary + ' msg_details=' + msg_details)
f.close()
