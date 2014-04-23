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
version =    "1"
verdate =    "2014-03-04T13:02:00Z"
#
#
# Purpose:     Script to provide the interface to postzmsg to send onto Omnibus. 
#            The script is called from the splunk saved Search and will parse
#            csv file with specific Headers.
#
#
# *************************************************************************************

# *************************************************************************************
# Logging Configurations
# *************************************************************************************
TODAY_YYYYMMDD     =    time.strftime("%Y%m%d")
LOG_DIR            =    '/tmp/'
LOG_FILENAME       =    'Splunk_to_Tivoli.' + TODAY_YYYYMMDD + '.log'
LOG_ABSFILE        =    LOG_DIR + LOG_FILENAME
logging.basicConfig(filename=LOG_ABSFILE, format='%(asctime)s - %(levelname)s - [%(process)d] - %(message)s', level=logging.INFO)

# *************************************************************************************
# Script Info
# *************************************************************************************
INPUT_PARAMS_LENGTH       =     len(sys.argv)
if(len(sys.argv) < 2):
    print "You must set argument!!!"
    print "Usage is : <scriptname> <inputFile>"
    logging.error('Wrong Usage: Input CSV File not specified')
    exit(2)
    
CSV_FILE_IN                =    sys.argv[1]
TEC_Source                 =    'Splunk_to_Tivoli'
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

logging.info('Starting Script ' + program)

# Check if SPLUNK has been created required input file. 
# IF no file, then assume no alert to parse/send and exit
if not os.path.isfile(CSV_FILE_IN_ABS):
    logging.info('File ' + CSV_FILE_IN_ABS + ' NOT present. NO alerts to send')
	logging.info('Ending Script ' + program)
    sys.exit()

# Checking if Tivoli scripts/Configs are present. IF NOT throw error and exit
if not os.path.isfile(TIVOLI_SCRIPT):
    logging.error('File ' + TIVOLI_SCRIPT + ' NOT present. Exiting without sending alerts')
    sys.exit()
    
if not os.path.isfile(TIVOLI_CFG):
    logging.error('File ' + TIVOLI_CFG + ' NOT present. Exiting without sending alerts')
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
    logging.error('Unable to Copy Temp file ' + TEMP_FILE + ' . May be permission issue. Exiting without any action')
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
logging.info('Start Sending Alerts using ' + TIVOLI_SCRIPT)

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
            
        CAT_TEC_Severity          =    '-r ' + realVal[0]
        CAT_TEC_Message           =    '-m "' + realVal[1] + '"'
        CAT_TEC_AlertGroup        =    realVal[2]
        
        # Rest of the fields, could be anything. So concatenating everything to one String
        count    = 3
        CAT_ALLOTHER_FIELDS            =    ''
        while (count < ncol):
            CAT_ALLOTHER_FIELDS        =     CAT_ALLOTHER_FIELDS  + headerVal[count] + '="' + realVal[count] + '" '
            count = count + 1
        
        # command = ['echo',TIVOLI_SCRIPT,'-f',TIVOLI_CFG,CAT_TEC_Severity,CAT_TEC_Message,CAT_ALLOTHER_FIELDS,CAT_TEC_AlertGroup,TEC_Source]
        command = [TIVOLI_SCRIPT,'-f',TIVOLI_CFG,CAT_TEC_Severity,CAT_TEC_Message,CAT_ALLOTHER_FIELDS,CAT_TEC_AlertGroup,TEC_Source]
        try:
            subprocess.Popen(command)
        except OSError:
            logging.error('Unable to run Tivoli Script. Temp file ' + TEMP_FILE + ' not removed')
            sys.exit(2)

logging.info('Finished Sending Alerts using ' + TIVOLI_SCRIPT)
# End of Core logic ***************

# Remove any temporary files created
try:
    subprocess.call(['rm','-f',TEMP_FILE])
except OSError:
    logging.error('Unable to Remove Temp file ' + TEMP_FILE + '. Remove this manually')
    sys.exit(2)

logging.info('Ending Script ' + program)
# *************************************************************************************
# End of Script
# *************************************************************************************

