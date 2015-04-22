#!/bin/sh

# ============================================================================
# Simple install/uprade script for Splunk Enterprise
# Version : 0.1
# ============================================================================

# ============================================================================
# Amend This to fit infrastructure
# Softlink splunk installable for future upgrades
# ============================================================================
splunkInstallable="splunk-latest-linux-x86_64"
SPLUNK_HOME="/opt/splunk"
SPLUNKFWD_INITD="initd_splunkforwarder.file"

# ============================================================================
# Checks
# ============================================================================
if [[ $EUID -ne 0 ]]; then
   echo "Error: This script must be run as root" 1>&2
   exit 1
fi

if [ ! -f "$splunkInstallable" ]
then
  echo "Installable not found. Exiting without any changes"
  exit 1
fi


# ============================================================================
# #<Identify Relevant Environment> and Service
# ============================================================================
THISHOST=`uname -n`
INSTALLEDCHECK=`rpm -qa | grep splunk-`
rc=$?

# ============================================================================
# Check if Splunk is currently installeled
# ============================================================================
if [[ -n "$INSTALLEDCHECK" ]]
then
    ISINSTALLED="True"
    echo "Splunk version : $INSTALLEDCHECK installed. Will upgrade if possible"
    rpm -Uvh $splunkInstallable
    rc=$?

else
    ISINSTALLED="False"
    echo "Installing Splunk for first Time"
    rpm -ivh $splunkInstallable
    rc=$?
fi


if [ $rc != "0" ]
then
    echo "========================= ERROR ERROR ERROR ========================= "
    echo "Error occured during upgrade or installation. Please manually remove any directories created.. "
    echo "Quitting.. "
    echo "========================= ERROR ERROR ERROR ========================= "
    exit 100

else
    /bin/su - splunk -c "${SPLUNK_HOME}/bin/splunk start --no-prompt --answer-yes --accept-license"
    echo "Info: Successfully Configured Splunk"

fi

# enable boot-start should need to be done in init
# Copy init.d script too for automatic start/stop functionality
if [ -f "$SPLUNKFWD_INITD" ]; 
then
   cp $SPLUNKFWD_INITD /etc/init.d/splunk
   chmod 744 /etc/init.d/splunk
   chkconfig splunk on
else
   echo "***** init.d splunk entry not made. Splunk auto-start may NOT WORK *********"
fi

# ============================================================================
# End of Script
# ============================================================================
