#!/bin/sh

# ============================================================================
# Basic Script to Unsintall+Install Splunk Universal Forwarder in LINUX environments
# Version : 0.8 
# ============================================================================

# ============================================================================
# #<Identify Relevant Environment> and Service
# ============================================================================

# Dynamically find CLIENT_ENV
# your code here
# Deployment Server IP below
DEP_SERVER_IP="10.1.2.3"
# ============================================================================
# Constant values for Splunk
# ============================================================================

# PORTS 
DEP_PORT=8091
FWD_PORT=9997

# SPLUNK Installable 
# Link this to the correct version at OS level
SPLUNK_PKG_RPM="splunkforwarder-latest-x86-64.rpm"

# Set the new Splunk admin password
FWD_PASS="changeme"

SPLUNK_USER="splunk"
SPLUNK_HOME="/opt/splunkforwarder"
SPLUNK_ROOT="${SPLUNK_HOME}/../"
SPLUNKFWD_INITD="initd_splunkforwarder.file"

# ============================================================================
# Evaluate ${CLIENT_ENV}_SERVER_IP
# Find the equivalent Server IP from Destination Master Splunk IP List 
# ============================================================================


DEPLOY_SERVER="${DEP_SERVER_IP}:${DEP_PORT}"

# Check if the correct user is used
currentUser=`whoami`
if [ $currentUser != "root" ]
then
    echo  "Script should be run as root .. Exiting without any changes"
    exit 0
fi


# Generate Variables
DEPLOYMENT_CONFIG_DESTINATION="${SPLUNK_HOME}/etc/apps/deployclient/local"
DEPLOYMENT_CONFIG_FILE="${DEPLOYMENT_CONFIG_DESTINATION}/deploymentclient.conf"

# ========================= Uninstall Start =========================

# Remove Previous Splunk Fowarder Installation
rpm -q splunkforwarder | grep -vq "not installed" && isInstalled="TRUE" || isInstalled="FALSE" 
if [ $isInstalled == "TRUE" ]
then
    SPLUNKFWDVERSION=`rpm -q splunkforwarder`
    rpm -e $SPLUNKFWDVERSION
    rc=$?
fi

if [ $rc != "0" ]
then
    echo "Error occured during Uninstall. Please manually remove any directories created.. "
    echo "Quitting.. "
    exit 100
fi

# Delete any splunkforwarder Directories
if [ -d "$SPLUNK_HOME" ]; 
then
   rm -rf $SPLUNK_HOME
fi
# ========================= Uninstall End      =========================

# ========================= Installation Start =========================
# Copy init.d script too for automatic start/stop functionality
if [ -f "$SPLUNKFWD_INITD" ]; 
then
   cp $SPLUNKFWD_INITD /etc/init.d/splunk
   chmod 744 /etc/init.d/splunk
fi

# Actual Installation 
rpm -i $SPLUNK_PKG_RPM

rc=$?

if [ $rc != "0" ]
then
    echo "Error occured during installation. Please manually remove any directories created.. "
    echo "Quitting.. "
    exit 100
fi
# ========================= Installation End    =========================

# ========================= Configuration Start =========================
/bin/su $SPLUNK_USER -c "mkdir -p ${DEPLOYMENT_CONFIG_DESTINATION} "
/bin/su $SPLUNK_USER -c "touch ${DEPLOYMENT_CONFIG_FILE}"
rc=$?

# Build Deployment config or build it externally
echo '[deployment-client]' >> ${DEPLOYMENT_CONFIG_FILE}
echo '' >> ${DEPLOYMENT_CONFIG_FILE}
echo '[target-broker:deploymentServer]' >> ${DEPLOYMENT_CONFIG_FILE}
echo "targetUri = ${DEPLOY_SERVER}"  >> ${DEPLOYMENT_CONFIG_FILE}

# Disable defaults and start splunk
/bin/su $SPLUNK_USER -c "${SPLUNK_HOME}/bin/splunk edit user admin -password $FWD_PASS -auth admin:changeme --accept-license"
/bin/su $SPLUNK_USER -c "${SPLUNK_HOME}/bin/splunk set  splunkd-port $DEP_PORT "
/bin/su $SPLUNK_USER -c "${SPLUNK_HOME}/bin/splunk start "
# ========================= Configuration End =========================

# enable boot-start should need to be done in init
echo "**** ===================================================================== ****"
echo "**** Ensure /etc/init.d/splunk entry is present and contains valid entries ****"
echo "**** ===================================================================== ****"

echo ""
echo "**** Splunk Fowarders Successfully Installed ****"
echo ""
# ============================================================================
# End of Script
# ============================================================================
