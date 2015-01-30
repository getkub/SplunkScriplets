#!/bin/sh

# ============================================================================
# Basic Script to Manage Splunk (status/Install/Uninstall) in *NIX environments
# ============================================================================

# ============================================================================
# Script Usage
# ============================================================================
if [ $# -lt 1 ]
then
    echo "Error: Incorrect Usage. Usage is:    <scriptname> <status|uninstall|install> {0|1}" 1>&2
    exit 1
fi

# ============================================================================
# Check that this script has been executed under root
# ============================================================================
if [[ $EUID -ne 0 ]]; then
   echo "Error: This script must be run as root" 1>&2
   exit 1
fi

# ============================================================================
# Initial variables
# ============================================================================
OSTYPE=`uname`
INSTALLEDCHECK=`rpm -qa | grep splunk-`
BASEDIR="/home/deploy"
SPLUNK_HOME="/opt/splunk"
INPUT_OPTION=$1
OUTPUT=""
INSTALL_RPM=`ls ${BASEDIR}/Installables/splunk-*.rpm | tail -1`
RC=0
# ============================================================================
# Check OS Type
# ============================================================================
if [ $OSTYPE != "Linux" ]
then
    echo "Error: Deployment script is not designed for this OS type." 1>&2
    exit 1
fi

# ============================================================================
# Check if Splunk is currently installeled
# ============================================================================
if [[ -n "$INSTALLEDCHECK" ]]
then
    ISINSTALLED="True"
else
    ISINSTALLED="False"
fi


# ============================ PART1 ================================================
# ============================================================================
# Splunk Status Check
# ============================================================================
if [ "$INPUT_OPTION" == "status" ]
then
    echo "#########################################"
    echo "        Splunk Deployment Status         "
    echo ""
    echo "        Installed - $ISINSTALLED         "
    echo ""
    if [ "$ISINSTALLED" == "True" ]
    then
        echo " Build   - $INSTALLEDCHECK"
        echo ""
        echo "#########################################"
    else
        echo "#########################################"
    fi

    exit 0
fi

# ============================ PART2 ================================================
# ============================================================================
# Splunk Uninstall
# ============================================================================
if [ "$INPUT_OPTION" == "uninstall" ]
then
    echo "Info: Uninstalling Splunk"
    if [[ -n "$INSTALLEDCHECK" ]]
    then
    echo "Info: $INSTALLEDCHECK installed, removing"
        OUTPUT=$(rpm -e $INSTALLEDCHECK)
        RC=$?
                OUTPUT=`rm -rf ${SPLUNK_HOME}/etc`
                t=$?
                RC=$((RC+t))
        if [ "$RC" == "0" ]
        then
                   sleep 5
           echo "Info: Splunk successfully uninstalled"
           t=`rm /etc/init.d/splunk; echo $?`
           RC=$((RC+t))
           t=`chkconfig splunk off` # To unset run level  in /etc/init.d/rc2.d/
           RC=$((RC+t))
           if [ "$RC" == "0" ]
           then
              echo "Info: Splunk Uninstall Successful"
           else
              echo "Warn: Cannot remove items completely. Manually remove it"
           fi
        else
           echo "Error: Splunk Uninstall NOT Successful"
           echo "Info:  Uninstall Splunk manually"
        fi

    else
        echo "Info: No previous installation Found. Exiting without any action"
    fi
    exit 0
fi

# ============================ PART3 ================================================
# ============================================================================
# Splunk Deploy/Install
# ============================================================================
if [ "$INPUT_OPTION" != "install" ]
then
    echo "Error: Accepted Options are limited to status|uninstall|install" 1>&2
    exit 1
fi

# ============================================================================
# Now install Splunk RPM
# ============================================================================
INSTALLPACKAGE=`basename ${INSTALL_RPM}`
if [ -z "$INSTALL_RPM" ]; then
   echo "Error: Unable to find RPM to install"
   exit 255
fi

echo "Info: Installing Splunk"
rpm -ivh ${BASEDIR}/Installables/${INSTALLPACKAGE}
RC=$?
if [ "$RC" != "0" ]
then
   echo "Error: Splunk Install NOT Successful"
   exit 255
else
   chkconfig splunk off   # To unset run level  in /etc/init.d/rc2.d/
   # chkconfig splunk     # Check current level
   chkconfig splunk 2     # to set run level
   # /bin/su - splunk -c "\"/opt/splunk/bin/splunk\" start --no-prompt --answer-yes --accept-license"
   echo "Info: Successfully Installed Splunk"
fi

# ============================================================================
#  End of Script
# ============================================================================
