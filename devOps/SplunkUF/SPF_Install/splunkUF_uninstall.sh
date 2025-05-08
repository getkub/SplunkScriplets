#!/bin/sh

# ============================================================================
# Splunk Universal Forwarder Uninstall Script for Linux
# Version: 1.0
# ============================================================================

COMPONENT="SplunkUninstall"
LOGFILE="/var/log/splunk_uninstall.log"
SPLUNK_HOME="/opt/splunkforwarder"
SPLUNK_USER="splunkfwd"

log() {
    local level=$1
    local msg=$2
    echo "$(date +'%Y-%m-%d %H:%M:%S') - component=${COMPONENT}, level=${level}, message=${msg}" | tee -a "$LOGFILE"
}

# ============================================================================
# Root Check
# ============================================================================
if [ "$EUID" -ne 0 ]; then
    log "ERROR" "This script must be run as root."
    exit 1
fi

log "INFO" "Starting Splunk Universal Forwarder uninstall."

# ============================================================================
# Stop splunkforwarder service if SPLUNK_HOME exists
# ============================================================================
if [ -d "$SPLUNK_HOME" ]; then
    log "INFO" "Splunk home directory found, stopping Splunk Forwarder."
    "${SPLUNK_HOME}/bin/splunk" stop --accept-license --no-prompt
    log "INFO" "Stopped Splunk Forwarder using splunk CLI."
else
    log "WARN" "Splunk home directory not found. Skipping stop command."
fi

# ============================================================================
# Remove Splunk package
# ============================================================================
if command -v rpm > /dev/null 2>&1; then
    rpm -e splunkforwarder 2>/dev/null && log "INFO" "Removed RPM package." || log "INFO" "RPM package not found."
elif command -v dpkg > /dev/null 2>&1; then
    dpkg -r splunkforwarder 2>/dev/null && log "INFO" "Removed DEB package." || log "INFO" "DEB package not found."
fi

# ============================================================================
# Remove Splunk installation directory
# ============================================================================
if [ -d "$SPLUNK_HOME" ]; then
    rm -rf "$SPLUNK_HOME"
    log "INFO" "Removed Splunk directory $SPLUNK_HOME."
fi

# ============================================================================
# Optionally remove splunkfwd user
# ============================================================================
if id "$SPLUNK_USER" >/dev/null 2>&1; then
    userdel "$SPLUNK_USER" 2>/dev/null && log "INFO" "Deleted user $SPLUNK_USER." || log "WARN" "Failed to delete user $SPLUNK_USER."
else
    log "INFO" "User $SPLUNK_USER not present."
fi

log "INFO" "Splunk Universal Forwarder uninstalled successfully."
