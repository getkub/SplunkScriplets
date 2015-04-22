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
SPLUNKFWD_INITD="initd_splunkEnterprise.file"
SPLUNK_USER="splunk"
NEW_PASS="changeme_new"
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
    ACTION = "UPGRADE"
    echo "Splunk version : $INSTALLEDCHECK installed. Will upgrade if possible"
    rpm -Uvh $splunkInstallable
    rc=$?

else
    ISINSTALLED="False"
    ACTION = "INSTALL"
    echo "Installing Splunk for first Time"
    rpm -ivh $splunkInstallable
    rc=$?
fi


if [ $rc != "0" ]
then
    echo "========================= ERROR ERROR ERROR ========================= "
    echo "Error occured during $ACTION of Splunk"
    echo "Quitting.. "
    echo "========================= ERROR ERROR ERROR ========================= "
    exit 100

else
        # Disable defaults and start splunk
    /bin/su $SPLUNK_USER -c "touch  ${SPLUNK_HOME}/etc/.ui_login "
    /bin/su $SPLUNK_USER -c "${SPLUNK_HOME}/bin/splunk edit user admin -password $NEW_PASS -auth admin:changeme --accept-license --answer-yes --no-prompt"
    /bin/su $SPLUNK_USER -c "${SPLUNK_HOME}/bin/splunk start --no-prompt --answer-yes --accept-license"
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
