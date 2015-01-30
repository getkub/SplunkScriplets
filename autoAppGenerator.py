#!/usr/bin/python
import csv
import os
import re
import sys

# ============================================================================
# Basic Script to Create Splunk Apps from Command-line
# Will generate app.conf, inputs.conf & outputs.conf based on configuration
# ============================================================================

# ============================================================================
# Requires Directory with all elements to create barebone app
# ============================================================================

# Parameters
TEMPLATE_NAME           ='SPK_FWDAPP_TEMPLATE'
TEMPLATE_NEW            ='SPK_FWDAPP_TEMPLATE_COPY'
TEMPLATE_LOCATION       = './'
csvFileInput            = TEMPLATE_LOCATION + 'AppConfig.csv'
# SERVERCLASSFILE         = TEMPLATE_LOCATION + 'serverclass.conf'
# osCommand = 'rm -rf ' + SERVERCLASSFILE
# os.system(osCommand)  # Removes any old serverclass.conf file
# ============================================================================

# ===========================
# Config Files for Splunk that needs editing
# Write this with respect to base directory
# ===========================
APPCONFIG = 'default/app.conf'
APPCONF_FILE_TEMPLATE= """
#
# Splunk app configuration file
# Created using Template
#

[install]
is_configured = 0

[ui]
is_visible = {___APPCONF__is_visible___}
label = {___APPCONF__label___}

[launcher]
author = {___APPCONF__author___}
description = {___APPCONF__description___}
version = {___APPCONF__version___}

"""
# ===========================

INPUTCONF = 'local/inputs.conf'
INPUTCONF_FILE_TEMPLATE= """
[monitor://{___INPUTCONF_monitor___}]
index  = {___INPUTCONF_index___}
source = {___INPUTCONF_source___}
sourcetype = {___INPUTCONF_sourcetype___}
"""
# ===========================
OUTPUTCONF = 'local/outputs.conf'
OUTPUTCONF_FILE_TEMPLATE= """
[tcpout]
defaultGroup = {___OUTPUTCONF_defaultGroup___}

[tcpout:{___OUTPUTCONF_defaultGroup___}]
server = {___OUTPUTCONF_server___}
autoLB = true

"""
# ===========================

# SERVICE,ENV,HOSTNAME,IPADDR,APPTYPE,APPTAG,AUTHOR,VERSION,LOGLOCATION,INDEX,DESCRIPTION,EOD


# Copies the Template to new Directory
# shUtil not working properly. Hence using os command to copy

# ============================================================================
# Generate the parameters accordingly
# ============================================================================
# filter(lambda row: row[0]!='#', fp)

# reader1 does all the file-level actions
reader1 = csv.reader(filter(lambda row: row[0]!='#',open(csvFileInput, 'rb')))
for row in reader1:
        FWD_SERVICE  =         row[0]
        FWD_ENV      =         row[1]
        FWD_HOSTNAME =         row[2]
        FWD_IPADDR   =         row[3]
        FWD_APPTYPE  =         row[4]
        FWD_APPTAG   =         row[5]
        FWD_AUTHOR   =         row[6]
        FWD_VERSION  =         row[7]
        FWD_LOGLOCATION =      row[8]
        VME_INDEX_NAME  =      row[9]
        FWD_DESCRIPTION =      row[10]
        FWD_SOURCETYPE  =      row[11]
        APPNAME = FWD_SERVICE + '_' + FWD_ENV + '_' +  FWD_APPTYPE + '-' + FWD_APPTAG
        APPLABEL = 'FWD_' + APPNAME
        osCommand = 'rm -rf ' + APPNAME
        os.system(osCommand)
        osCommand = 'cp -rf ' + TEMPLATE_NAME + ' ' + APPNAME
        os.system(osCommand)

# reader2 does all the data-level actions
reader2 = csv.reader(filter(lambda row: row[0]!='#',open(csvFileInput, 'rb')))
for row in reader2:
        FWD_SERVICE  =         row[0]
        FWD_ENV      =         row[1]
        FWD_HOSTNAME =         row[2]
        FWD_IPADDR   =         row[3]
        FWD_APPTYPE  =         row[4]
        FWD_APPTAG   =         row[5]
        FWD_AUTHOR   =         row[6]
        FWD_VERSION  =         row[7]
        FWD_LOGLOCATION =      row[8]
        VME_INDEX_NAME  =      row[9]
        FWD_DESCRIPTION =      row[10]
        FWD_SOURCETYPE  =      row[11]
        SPLUNK_INDEXERS =      eval(FWD_SERVICE + '_' + FWD_ENV + '_INDEXERS')
        INDEXER_GROUP = FWD_SERVICE + '_' + FWD_ENV + '_INDEXES'
        APPNAME = FWD_SERVICE + '_' + FWD_ENV + '_' +  FWD_APPTYPE + '-' + FWD_APPTAG
        SOURCE_NEW_ARRAY = FWD_LOGLOCATION.split('/')
        SOURCE_NEW = SOURCE_NEW_ARRAY[-1]
        # =====================================================================
        # Below code creates ./default/app.conf
        # Overwriting is not a problem
        # =====================================================================
        context = {
         "___APPCONF__is_visible___":'0',
         "___APPCONF__label___":APPLABEL,
         "___APPCONF__author___": FWD_AUTHOR,
         "___APPCONF__description___": FWD_DESCRIPTION,
         "___APPCONF__version___" : FWD_VERSION
         }
        tmpFile    = APPNAME + '/' + APPCONFIG
        fw = open(tmpFile, 'w')
        fw.write(APPCONF_FILE_TEMPLATE.format(**context))
        fw.close()

        # =====================================================================
        # Below code appends ./local/inputs.conf
        # if entry DOES NOT exist, it append previous inputs.conf file
        # if Entry exists, it skips
        # =====================================================================
        context = {
                 "___INPUTCONF_monitor___":FWD_LOGLOCATION,
                 "___INPUTCONF_source___":SOURCE_NEW,
                 "___INPUTCONF_index___":VME_INDEX_NAME,
                 "___INPUTCONF_sourcetype___":FWD_SOURCETYPE
         }
        tmpFile    = APPNAME + '/' + INPUTCONF
        found = True
        if os.path.exists(tmpFile):
            with open(tmpFile, "r+") as fr:
                for line in fr:
                    if re.search(FWD_LOGLOCATION, line):
                        found = False

                if     found:
                    fr.write(INPUTCONF_FILE_TEMPLATE.format(**context))
                    fr.truncate()

        else:
            fw = file(tmpFile, "w")
            fw.write(INPUTCONF_FILE_TEMPLATE.format(**context))
            fw.close()
        # =====================================================================
        # Below code appends ./local/outputs.conf
        # Will overwrite previous outputs.conf file
        # =====================================================================
        context = {
         "___OUTPUTCONF_defaultGroup___":INDEXER_GROUP,
         "___OUTPUTCONF_server___":SPLUNK_INDEXERS
         }
        tmpFile    = APPNAME + '/' + OUTPUTCONF
        fw = open(tmpFile, 'w')
        fw.write(OUTPUTCONF_FILE_TEMPLATE.format(**context))
        fw.close()

        osCommand = 'chown -R splunk:splunk ' + APPNAME
        os.system(osCommand)


# ============================================================================
# End of Script
# ============================================================================
