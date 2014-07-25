
#!/usr/bin/python
import csv, time
import os, subprocess
import sys, getopt
import logging


# *************************************************************************************
# Created:         getkub  ( I'm no python coder, hence some methods are crude)
# Name:            Splunk_to_Tivoli.py
#
program =    sys.argv[0]
version =    "2"
verdate =    "2014-05-23T13:02:00Z"
#
#
# Purpose:     Script to provide the interface to postzmsg to send onto Omnibus.
#            The script is called from the splunk saved Search and will parse
#            csv file with specific Headers.
#
# Version History
#
#     Version    Date      Comment
#       1       2014-03-04 Initial Version
#       2       2014-05-23 Changed logic to merge Array as Omnibus not detecting quotes
#
# *************************************************************************************

# *************************************************************************************
# Logging Configurations
# *************************************************************************************
TODAY_YYYYMMDD     =    time.strftime("%Y%m%d")
APP_DIR            =    os.path.dirname(os.path.dirname(os.path.dirname(program)))
LOG_DIR            =    APP_DIR + '/logs'
LOG_FILENAME       =    'Splunk_to_Tivoli.' + TODAY_YYYYMMDD + '.log'
LOG_ABSFILE        =    LOG_DIR + '/' + LOG_FILENAME
logging.basicConfig(filename=LOG_ABSFILE, format='%(asctime)s - %(levelname)s - [%(process)d] - %(message)s', level=logging.INFO)

# *************************************************************************************
# Script Info
# *************************************************************************************
INPUT_PARAMS_LENGTH       =     len(sys.argv)
logging.debug('Number of arguments=' + str(INPUT_PARAMS_LENGTH))
logging.debug('Argument list:' + str(sys.argv))
# Splunk Documentation: http://docs.splunk.com/Documentation/Splunk/6.1.1/Alert/Configuringscriptedalerts

if(len(sys.argv) < 9):
    print "You must set 9 arguments!!"
    print "Usage is : <scriptname> <arg1> <arg2> <arg3> <arg4> <arg5> <arg5> <arg6> <arg7> <arg8> <arg9>"
    logging.error('Wrong Usage - Seems Script Not triggered via Splunk')
    exit(2)

CSV_FILE_IN                =    sys.argv[4] + '.csv'
COUNT_ALERTS               =    sys.argv[1]
UNIQUE_URL                 =    sys.argv[6]
TEC_Source                 =    'Splunk_to_Tivoli_v4'
# *************************************************************************************
# Script Parameters
# *************************************************************************************
SPLUNK_HOME          = '/opt/splunk/'
TIVOLI_CFG           = '/etc/Tivoli/tivoli.conf'
TIVOLI_SCRIPT        = '/etc/Tivoli/bin/postzmsg'

CSV_DIR              = SPLUNK_HOME + 'var/run/splunk/'
CSV_FILE_IN_ABS      = CSV_DIR + CSV_FILE_IN

# *************************************************************************************
# Various Checks Done
# Add more checks/validations to create stable script
# *************************************************************************************

logging.info('Starting Script: ' + program)

# Check if SPLUNK has been created required input file.
# IF no file, then assume no alert to parse/send and exit
if not os.path.isfile(CSV_FILE_IN_ABS):
    logging.info('File: ' + CSV_FILE_IN_ABS + ' NOT present. NO alerts to send')
    logging.info('Ending Script: ' + program)
    sys.exit()

# Checking if Tivoli scripts/Configs are present. IF NOT throw error and exit
if not os.path.isfile(TIVOLI_SCRIPT):
    logging.error('File: ' + TIVOLI_SCRIPT + ' NOT present. Exiting without sending alerts')
    sys.exit()

if not os.path.isfile(TIVOLI_CFG):
    logging.error('File: ' + TIVOLI_CFG + ' NOT present. Exiting without sending alerts')
    sys.exit()

# Creates Temporary Dir and Temporary file
# Temporary file to copy CSV file and work with and delete
# This would have of format <filename>.<timestamp>.tmp to accomodate multiple runs
ts                      =    time.time()
SCRIPT_DIR              =    os.path.dirname(program)
TEMP_DIR                =    SCRIPT_DIR + '/STEMP/'
TEMP_FILE               =    TEMP_DIR + CSV_FILE_IN + '.' + str(ts) + '.tmp'

try:
    subprocess.call(['mkdir','-p',TEMP_DIR])
    subprocess.call(['cp',CSV_FILE_IN_ABS,TEMP_FILE])
except OSError:
    logging.error('Unable to Copy Temp file: ' + TEMP_FILE + ' . May be permission issue. Exiting without any action')
    sys.exit(2)

# *************************************************************************************
# Mandatory fields to Tivoli postzmsg
# http://publib.boulder.ibm.com/tividd/td/tec/SC32-1232-00/en_US/HTML/ecormst33.htm
# This script expects input file with first 3 fields mandatory
# Severity,Message,AlertGroup,<field_4>,<field_5> .... <field_n>
# *************************************************************************************

# *************************************************************************************
# Source is hardcoded as "Splunk_to_Tivoli"
# Bit clunky, but to extract headers and real Data, I'm reading the input file twice !!
# *************************************************************************************
# countLines = len(open(TEMP_FILE).readlines(  ))  # Not required as CSV file is produced only if there is data
logging.info('Start Sending Alerts using: ' + TIVOLI_SCRIPT + ', File=' + CSV_FILE_IN_ABS)
logging.info('ALERTCOUNT=' + str(COUNT_ALERTS) + ' ,URL=' + str(UNIQUE_URL))

# Reading Headers
with open(TEMP_FILE) as hdr:
    chdr = csv.reader(hdr)
    for row in chdr:
        ncol = len(row)
        count = 0
        headerVal = []
        while (count < ncol):
            headerVal.append(row[count])
            count = count + 1

        break    # Break from "for" loop

# Reading real data/values
with open(TEMP_FILE) as f:
    cf = csv.reader(f)
    next(cf,None)
    for row in cf:
        count = 0
        realVal = []
        while (count < ncol):
            realVal.append(row[count])
            count = count + 1

        TEC_Severity          =    realVal[0]
        TEC_Message           =    realVal[1]
        TEC_AlertGroup        =    realVal[2]

        # Rest of the fields, could be anything. So putting all of then into single array
        count    = 3
        OTHER_FIELDS_ARRAY            =    []
        while (count < ncol):
            OTHER_FIELDS_ARRAY.append(headerVal[count] + '=' + realVal[count])
            count = count + 1

        FINAL_ARRAY = [TIVOLI_SCRIPT,'-f',TIVOLI_CFG,'-r',TEC_Severity,'-m',TEC_Message] + OTHER_FIELDS_ARRAY[:] + [TEC_AlertGroup,TEC_Source]
        logging.debug(FINAL_ARRAY[:])
        try:
           p = subprocess.Popen(FINAL_ARRAY)
        except OSError:
            logging.error('Unable to run Tivoli Script. Temp file: ' + TEMP_FILE + ' not removed')
            sys.exit(2)


logging.info('Finished Sending Alerts using: ' + TIVOLI_SCRIPT)
# End of Core logic ***************

# Remove any temporary files created
try:
    subprocess.call(['rm','-f',TEMP_FILE])
except OSError:
    logging.error('Unable to Remove Temp file: ' + TEMP_FILE + '. Remove this manually')
    sys.exit(2)

logging.info('Ending Script: ' + program)
# *************************************************************************************
# End of Script
# *************************************************************************************
