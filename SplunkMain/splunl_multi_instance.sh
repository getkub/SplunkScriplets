#!/bin/sh

#------------------------------------------------
# Custom Script to install multi instances of 
# SPLUNK in specificied physical machines
#
#------------------------------------------------
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

thisHost=`hostname`
# ============================================================================

# List of machine hostnames and instances required
machine1=myhostname1
SPLUNK_ES1="splunkAUX splunkSI"
SPLUNK_UF1="splunkUF"

machine2=myhostname2
SPLUNK_ES2="splunkSH splunkSI"
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
echo " ---- Installing ${i} ----------"
echo "==========================================================================="
rpm --force -Uvh --prefix /opt/${i} ${splunk_es} 
/opt/${i}/splunk/bin/splunk enable boot-start -user splunk --accept-license --answer-yes --no-prompt
done

for i in `echo $listUF`
do
echo "==========================================================================="
echo " ---- Installing ${i} ----------"
echo "==========================================================================="
rpm --force -Uvh --prefix /opt/${i} ${splunk_uf}
/opt/${i}/splunkforwarder/bin/splunk enable boot-start -user splunk --accept-license --answer-yes --no-prompt
done

####  End of Script #############
