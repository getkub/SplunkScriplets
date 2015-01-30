#!/bin/sh

#########################################################
#
# Splunk Apps Create/Install Script
# This script will package up (create) from dev Server
# Installs them into other servers like prod
#
#########################################################
if [ $# -ne 2 ]
then
        echo "Error: Input Action & PackageName"
        echo "eg <scriptname> <create|install> <mypackage>"
        exit 1
fi

# Check that this script has been executed under splunk
CURRENT_USER=`whoami`
if [ "$CURRENT_USER" != "splunk" ]; then
   echo "Error: This script must be run as splunk user"
   exit 1
fi

ACTION=$1
INPUT_PACKAGE=$2
SPLUNK_DEV_DIR="/home/deploy"
SPLUNK_APPS_DIR="${SPLUNK_DEV_DIR}/SPLUNK_APPS"
TODAY=`date +%Y%m%d`
RUNTIME=`date +%Y%m%d-%H%M%S`
SPLUNK_HOME="/opt/splunk"
APPS_DIR="${SPLUNK_HOME}/etc/apps"
PKG_DIR="${SPLUNK_APPS_DIR}/pkg"
SCRIPTS_DIR="${SPLUNK_APPS_DIR}/scripts"
LOG_FILE="${SPLUNK_APPS_DIR}/logs/create.log.${TODAY}"
extn="tgz"
pkgApp="${APPS_DIR}/${INPUT_PACKAGE}"
pkgFile="${PKG_DIR}/${INPUT_PACKAGE}.${extn}"
backup_DIR="${SPLUNK_APPS_DIR}/bkup"

echo "${RUNTIME} Info:Starting Script ${INPUT_PACKAGE} "  >> $LOG_FILE

if [ $ACTION = "create" ] ; then

	if [ ! -d "${SPLUNK_APPS_DIR}" ]; then
	  echo "Error: No ${SPLUNK_APPS_DIR} present." | tee -a ${LOG_FILE}
	  exit 1
	fi

	if [ ! -d "${APPS_DIR}/${INPUT_PACKAGE}" ]; then
	  echo "Error: No Directory present for Package ${INPUT_PACKAGE} . Cannot create package" | tee -a ${LOG_FILE}
	  exit 1
	fi

	if [ -x  "${APPS_DIR}/${INPUT_PACKAGE}/rules/CreateRules.sh" ]; then
		echo "Custom Rules Existing. Now Configuring..."
		${APPS_DIR}/${INPUT_PACKAGE}/rules/CreateRules.sh
	fi


	cd ${APPS_DIR}; tar czf ${pkgFile} ${INPUT_PACKAGE} ; RC=$?
	if [ $RC -ne 0 ]; then
			echo "Error: Unable to pkg app. Exiting"  | tee -a ${LOG_FILE}
			exit 1
	else
			cp ${pkgFile} ${backup_DIR}/${INPUT_PACKAGE}.${RUNTIME}.${extn}
			echo "Info: Successfully Created pkg ${INPUT_PACKAGE}" | tee -a ${LOG_FILE}
	fi

elif [ $ACTION = "install" ] ; then

	if [ ! -d "${SPLUNK_APPS_DIR}" ]; then
	  echo "Error: No ${SPLUNK_APPS_DIR} present." | tee -a ${LOG_FILE}
	  exit 1
	fi

	if [ -d "${APPS_DIR}/${INPUT_PACKAGE}" ]; then
			cd ${APPS_DIR};
			tar czf ${backup_DIR}/${INPUT_PACKAGE}.${RUNTIME}.${extn} ${INPUT_PACKAGE};
			rm -rf ${APPS_DIR}/${INPUT_PACKAGE}
	fi

	cd ${APPS_DIR}
	cp ${pkgFile} ${APPS_DIR};
	tar xzf ${INPUT_PACKAGE}.${extn}
	RC=$?
	rm ${APPS_DIR}/${INPUT_PACKAGE}.${extn}

	if [ -x  "${APPS_DIR}/${INPUT_PACKAGE}/rules/InstallRules.sh" ]; then
		echo "Custom Rules Existing. Now Configuring..."
		${APPS_DIR}/${INPUT_PACKAGE}/rules/InstallRules.sh
	fi

	if [ $RC -ne 0 ]; then
			echo "Error: Unable to pkg app. Exiting"  | tee -a ${LOG_FILE}
			exit 1
	else
			echo "Info: Successfully Installed pkg ${INPUT_PACKAGE}" | tee -a ${LOG_FILE}
	fi

else

 echo 'Enter either "create" or "install" in command line'

fi


echo "${RUNTIME} : Ending Script ${INPUT_PACKAGE} "  >> $LOG_FILE
