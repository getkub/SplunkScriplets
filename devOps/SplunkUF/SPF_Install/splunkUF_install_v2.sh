#!/bin/sh

# ============================================================================
# Basic Script to Uninstall+Install Splunk Universal Forwarder in LINUX environments
# Version : 1.11
# ============================================================================

# ============================================================================
# Identify Relevant Environment and Service
# ============================================================================
OSTYPE=$(uname -s)
LOGFILE="/var/log/splunk_install.log"
COMPONENT="SplunkInstall"

log() {
    local level=$1
    local msg=$2
    echo "$(date +'%Y-%m-%d %H:%M:%S') - component=${COMPONENT}, level=${level}, message=${msg}" | tee -a "$LOGFILE"
}

log "INFO" "Starting Splunk Universal Forwarder installation script."

if [ "$OSTYPE" != "Linux" ]; then
    log "ERROR" "OSTYPE is not Linux. Exiting without any changes."
    exit 0
fi

# ============================================================================
# Constants
# ============================================================================
DEP_SERVER_IP="10.1.2.3"
SPLUNK_PKG_RPM="splunkforwarder-latest-x86-64.rpm"
SPLUNK_PKG_DEB="splunkforwarder-latest-amd64.deb"
FWD_PASS="changeme_new"
SPLUNK_HOME="/opt/splunkforwarder"
DEP_PORT=8089
DEPLOY_SERVER="${DEP_SERVER_IP}:${DEP_PORT}"

# ============================================================================
# Pre-Checks
# ============================================================================
if [ "$EUID" -ne 0 ]; then
    log "ERROR" "This script must be run as root."
    exit 1
fi

# Check for port conflicts *before install*
log "INFO" "Checking for port ${DEP_PORT} conflicts before installation."

if command -v netstat > /dev/null 2>&1; then
    if netstat -tuln | grep -q ":${DEP_PORT}"; then
        log "WARN" "Port ${DEP_PORT} is already in use. Installation may not bind correctly."
    fi
elif command -v ss > /dev/null 2>&1; then
    if ss -tuln | grep -q ":${DEP_PORT}"; then
        log "WARN" "Port ${DEP_PORT} is already in use. Installation may not bind correctly."
    fi
else
    log "WARN" "Neither netstat nor ss found. Skipping port conflict check."
fi

# Determine package type
if command -v rpm > /dev/null 2>&1; then
    PKG_TYPE="rpm"
    SPLUNK_PKG="$SPLUNK_PKG_RPM"
    log "INFO" "RPM system detected."
elif command -v dpkg > /dev/null 2>&1; then
    PKG_TYPE="deb"
    SPLUNK_PKG="$SPLUNK_PKG_DEB"
    log "INFO" "DEB system detected."
else
    log "ERROR" "Neither RPM nor DEB detected. Cannot proceed."
    exit 2
fi

if [ ! -f "$SPLUNK_PKG" ]; then
    log "ERROR" "Splunk package $SPLUNK_PKG not found in current directory."
    exit 2
fi

# ============================================================================
# Installation
# ============================================================================
log "INFO" "Installing Splunk Universal Forwarder from $SPLUNK_PKG."

if [ "$PKG_TYPE" = "rpm" ]; then
    rpm -U "$SPLUNK_PKG"
elif [ "$PKG_TYPE" = "deb" ]; then
    dpkg -i "$SPLUNK_PKG"
fi

if [ "$?" -ne 0 ]; then
    log "ERROR" "Installation failed. Please remove any partial install manually."
    exit 100
fi

# ============================================================================
# Configuration
# ============================================================================
log "INFO" "Configuring Splunk: setting password and deployment server."

mkdir -p "${SPLUNK_HOME}/etc/apps/deployclient/local"
cat <<EOF > "${SPLUNK_HOME}/etc/apps/deployclient/local/deploymentclient.conf"
[deployment-client]
[target-broker:deploymentServer]
targetUri = ${DEPLOY_SERVER}
EOF

"${SPLUNK_HOME}/bin/splunk" edit user admin -password "$FWD_PASS" -auth admin:changeme --accept-license --answer-yes --no-prompt
"${SPLUNK_HOME}/bin/splunk" set splunkd-port "$DEP_PORT"
"${SPLUNK_HOME}/bin/splunk" start --accept-license --answer-yes --no-prompt

if [ "$?" -ne 0 ]; then
    log "ERROR" "Splunk failed to start. Please check logs and directories manually."
    exit 101
fi

# ============================================================================
# Enable and Start Service
# ============================================================================
log "INFO" "Enabling and starting splunkforwarder service."

if command -v systemctl > /dev/null 2>&1; then
    systemctl enable splunkforwarder
    systemctl start splunkforwarder
    log "INFO" "Splunk Forwarder service started via systemd."
else
    log "WARN" "Systemd not found. Please enable/start splunkforwarder manually."
fi

log "INFO" "**** Splunk Forwarder Successfully Installed ****"
