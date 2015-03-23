
#!/bin/sh

# ============================================================================
# Script to configure Splunk after first Deploy
# Version : 0.1
# ============================================================================

# ============================================================================
# Check that this script has been executed under root
# ============================================================================
if [[ $EUID -ne 0 ]]; then
   echo "Error: This script must be run as root" 1>&2
   exit 1
fi

install_path="/home/deploy"
# Use a script or something to fetch environment details
# ServiceName=`myenvScript` 
ServiceName=`getEnvironment` 

# DS - Deployment Server
# SH - Splunk Head
# SI - Splunk Indexer
# DS_SH_SI - combination  etc.. in alphabetical order
SERVERTYPE=`getServerType`   

# Search Peers are other Peers
SearchPeers=`$getSearchPeers`

# ============================================================================
# #<Identify Relevant Environment> and Service
# ============================================================================
THISHOST=`uname -n`
INSTALLEDCHECK=`rpm -qa | grep splunk-`
SPLUNK_HOME="/opt/splunk"
SPLUNK_CRED="newchangeme"
ADM_PORT="8071"
RC=0
# ============================================================================
# Check if Splunk is currently installeled
# ============================================================================
if [[ -n "$INSTALLEDCHECK" ]]
then
    ISINSTALLED="True"
else
    ISINSTALLED="False"
    echo "Warn: Splunk not installed. Exiting without any changes!"
    exit 1
fi


if [ "$ServiceName" != "$THISHOST" ];then
   echo "Error: Unable to find ${THISHOST} in main configuration. Exiting without any actions..."
   exit 2
fi

echo "Info: Starting to Configure Splunk"
echo "Info: Stopping Splunk if its already running"
/bin/su - splunk -c "/opt/splunk/bin/splunk stop "

# ============================================================================
# Copy required files
# ============================================================================
echo "Info: Copying required files"
${install_path}/myEnv/scripts/copyFiles.py ${install_path}/myEnv/configs/csv/INITIAL_Deploy_Files.csv

# ============================================================================
# Install Default Apps
# ============================================================================
# Cheap way to filter
if [ "$SERVERTYPE" == "SH_SI" ]; then
   BaseApps="sos"
elif [ "$SERVERTYPE" == "SH" ]; then
   BaseApps="sideview_utils sos"
elif [ "$SERVERTYPE" == "SI" ]; then
   BaseApps="TA-sos"
fi
echo "Info: ServerType= $SERVERTYPE "

for appName in `echo $BaseApps`
do
 if [ ! -z "$BaseApps" ]
 then
   echo "Info: Installing APP: $appName "
   /bin/su - splunk -c "${install_path}/SPLUNK_APPS/scripts/install_pkg.sh $appName "
 fi
done

# ============================================================================
#  Re-Starting Splunk
# ============================================================================
/bin/su - splunk -c "touch  ${SPLUNK_HOME}/etc/.ui_login "
/bin/su - splunk -c "/opt/splunk/bin/splunk start --no-prompt --answer-yes --accept-license"

# ============================================================================
# Configure Search Peers
# ============================================================================
SearchPeers=`${install_path}/myEnv/scripts/getEnv.py | grep getSearchPeers| awk -F'=' '{print $2}'`

if [ "$SearchPeers" == "NA" ]
then
   echo "Info: No Search Peers to Configure"
else
   SearchPeersArray=(${SearchPeers//:/ })
   for peer in "${SearchPeersArray[@]}"
   do
       echo "Info: Adding Search Peer - ${peer}"
       /bin/su - splunk -c "/opt/splunk/bin/splunk add search-server -host ${peer}:$ADM_PORT -auth splunk:$SPLUNK_CRED -remoteUsername splunk -remotePassword $SPLUNK_CRED" ; j=$? ; RC=$(($j + $RC))
   done
fi

if [ $RC -ne 0 ]; then
   echo "Error: *** Search Peer configuration error *** "
   exit 1
fi

# Redirect Port 8000 to 443 for end users to login normally
# To display run: iptables -t nat -L -n -v
iptables -t nat -D PREROUTING -p tcp --dport 443 -j REDIRECT --to-ports 8000
iptables -t nat -A PREROUTING -p tcp --dport 443 -j REDIRECT --to-ports 8000
iptables-save > /etc/iptables.rules

echo "Info: Successfully Configured Splunk"

# ============================================================================
# End of Script
# ============================================================================
