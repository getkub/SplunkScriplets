#!/bin/sh

# ============================================================================
# Script to housekeep files based on days older than
# This could be then triggered from Splunk Schedule/Cron
# ============================================================================

# ============================================================================
# Check that this script has been executed under root
# ============================================================================
if [[ $EUID -ne 0 ]]; then
   echo "Error: This script must be run as root" 1>&2
   exit 1
fi

# ============================================================================
# Variables
# ============================================================================
daystoKeep=5

TODAY=`date +%Y%m%d`
BASEDIR="/home/deploy"
MODULE="HouseKeep"
LOGDIR="${BASEDIR}/${MODULE}/logs"
LOGFILE="${LOGDIR}/${MODULE}.log.${TODAY}"
# ============================================================================
# Actions
#============================================================================
DATADIR=${BASEDIR}/DATA
echo "Info: Checking Files to Housekeep " >> ${LOGFILE}
find ${DATADIR} -type f -mtime +${daystoKeep} -exec ls {} \; >> ${LOGFILE}

# Now deletign them
find ${DATADIR} -type f -mtime +${daystoKeep} -exec rm {} \;

echo "Info: Housekeeping Complete"  >> ${LOGFILE}

