#!/bin/sh

# ============================================================================
# Checks
# ============================================================================
# Check if the correct user is used
if [[ $EUID -ne 0 ]]; then
   echo "Error: This script must be run as root" 1>&2
   exit 1
fi

# Soft link the Splunk installables beforehand
splunk_es="splunk_es_x64.rpm"
splunk_uf="splunk_uf_x64.rpm"

if [[ ! -f ${splunk_es} || ! -f ${splunk_uf} ]]; then
    echo "Either of ${splunk_es} or ${splunk_uf} NOT found. Exiting ..."
    exit 1
fi

thisHost=`hostname -s`
# ============================================================================

# List of machine hostnames and instances required
machine1=myhost1
SPLUNK_ES1="splunkDEP splunkIDX"
SPLUNK_UF1="splunkUF"

machine2=myhost2
SPLUNK_ES2="splunkSH splunkIDX"
SPLUNK_UF2="splunkUF"

# Validate hostname to installation 
if [ ${machine1} == ${thisHost} ]; then
   listES=${SPLUNK_ES1}
   listUF=${SPLUNK_UF1}
elif [ ${machine2} == ${thisHost} ]; then
   listES=${SPLUNK_ES2}
   listUF=${SPLUNK_UF2}
else
   echo "Hostname not matching with provided list. Exiting without any action..."
   exit 2
fi

# ===========================================================================
# Install starts here
# ===========================================================================
for i in `echo $listES`
do
 
  echo "==========================================================================="
  echo " ---- Upgrading/Installing ${i} ----------"
  echo "==========================================================================="
   rpm --force -Uvh --prefix /opt/${i} ${splunk_es} 
   rc=$?
   echo "Upgrade/Install of $i Return Code = $rc"
   /opt/${i}/splunk/bin/splunk enable boot-start -user splunk --accept-license --answer-yes --no-prompt > /dev/null 2>&1 

done

for i in `echo $listUF`
do

  echo "==========================================================================="
  echo " ---- Upgrading/Installing ${i} ----------"
  echo "==========================================================================="
   rpm --force -Uvh --prefix /opt/${i} ${splunk_uf}
   rc=$?
   echo "Upgrade/Install of $i Return Code = $rc"
   /opt/${i}/splunkforwarder/bin/splunk enable boot-start -user splunk --accept-license --answer-yes --no-prompt > /dev/null 2>&1 

done

####  End of Script #############
