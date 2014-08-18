#!/bin/sh

# ============================================================================
# Basic Script to Unsintall+Install Splunk Universal Forwarder in LINUX environments
# Version : 1.02
# ============================================================================

# ============================================================================
# #<Identify Relevant Environment> and Service
# ============================================================================
ENVTYPE=`hostname | cut -c 7-8`
OSTYPE=`uname`
SITE=`hostname | cut -c 5-6`

if [ $OSTYPE != "Linux" ]
then
    echo "Unable to determine OSTYPE to be LINUX. Exiting without any changes"
    exit 0
fi

# ============================================================================
# Deployment Server Configuration
# ============================================================================
# Specify the Parent Splunk Deployment Server
# your code here to dynamically find  or from facter is installed add to facter?
# Deployment Server IP below
DEP_SERVER_IP="10.1.2.3"

# ============================================================================
# Constant values for Splunk
# ============================================================================

# PORTS 
DEP_PORT=8089
FWD_PORT=9997
DEPLOY_SERVER="${DEP_SERVER_IP}:${DEP_PORT}"

# SPLUNK Installable 
# Soft Link this to the correct version if you require
SPLUNK_PKG_RPM="splunkforwarder-latest-x86-64.rpm"

# Set the new Splunk admin password
FWD_PASS="changeme_new"
SPLUNK_USER="splunk"
SPLUNK_HOME="/opt/splunkforwarder"
SPLUNK_ROOT="${SPLUNK_HOME}/../"
SPLUNKFWD_INITD="initd_splunkforwarder.file"


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

# ========================= Upgrade Start =========================

# Actual Upgrade 
rpm -U $SPLUNK_PKG_RPM
rc=$?

if [ $rc != "0" ]
then
    echo "========================= ERROR ERROR ERROR ========================= "
    echo "Error occured during installation. Please manually remove any directories created.. "
    echo "Quitting.. "
    echo "========================= ERROR ERROR ERROR ========================= "
    exit 100
fi
# ========================= Installation End    =========================

# ========================= Configuration Start =========================
/bin/su $SPLUNK_USER -c "mkdir -p ${DEPLOYMENT_CONFIG_DESTINATION} "
/bin/su $SPLUNK_USER -c "> ${DEPLOYMENT_CONFIG_FILE}"
/bin/su $SPLUNK_USER -c "touch ${LOCALSYSTEM_CONFIG_FILE}"
rc=$?


# Build Deployment config
echo '[deployment-client]' >> ${DEPLOYMENT_CONFIG_FILE}
echo '' >> ${DEPLOYMENT_CONFIG_FILE}
echo '[target-broker:deploymentServer]' >> ${DEPLOYMENT_CONFIG_FILE}
echo "targetUri = ${DEPLOY_SERVER}"  >> ${DEPLOYMENT_CONFIG_FILE}

# If the $DEP_PORT is not available SPLUNK falls back to 8089. We don't want this. So forcing to $DEP_PORT else fail
echo '[settings]' > ${LOCALSYSTEM_CONFIG_FILE}
echo "mgmtHostPort = 127.0.0.1:${DEP_PORT}" >> ${LOCALSYSTEM_CONFIG_FILE}

# Disable defaults and start splunk
/bin/su $SPLUNK_USER -c "${SPLUNK_HOME}/bin/splunk edit user admin -password $FWD_PASS -auth admin:changeme --accept-license --answer-yes --no-prompt"
/bin/su $SPLUNK_USER -c "${SPLUNK_HOME}/bin/splunk set  splunkd-port $DEP_PORT "
/bin/su $SPLUNK_USER -c "${SPLUNK_HOME}/bin/splunk start --accept-license --answer-yes --no-prompt"
rc=$?

if [ $rc != "0" ]
then
    echo "========================= ERROR ERROR ERROR ========================= "
    echo "Error occured during starting Splunk. Please manually remove any directories created.. "
    echo "Quitting.. "
    echo "========================= ERROR ERROR ERROR ========================= "
    exit 100
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

echo ""
echo "**** Splunk Fowarders Successfully Installed ****"
echo ""
# ========================= Configuration End =========================

# ============================================================================
# End of Script
# ============================================================================
