#!/bin/bash

# ============================================================================
# Splunk Universal Forwarder Installation Script for Linux
# Version: 1.4
#
# Description:
# Installs and configures the Splunk Universal Forwarder (UF) on Linux systems.
#
# Supported Platforms:
# - Debian/Ubuntu (uses .deb)
# - RedHat/CentOS/Amazon Linux (uses .rpm)
#
# Features:
# - Detects OS and installs correct package
# - Sets up dedicated non-root user for Splunk UF
# - Enables Splunk to start automatically on boot via systemd
# - Configures deployment server
# - Skips admin user creation for minimal footprint
#
# Requirements:
# - This script **must be run as root** (e.g., with sudo)
# - SPLUNK_USER and SPLUNK_GROUP must already exist
# - Package files must be present in the current directory
#
# ============================================================================

# Exit if not run as root
if [[ "$EUID" -ne 0 ]]; then
  echo "ERROR: This script must be run as root. Use sudo or switch to root user."
  exit 1
fi

# Configuration Variables
SPLUNK_HOME="/opt/splunkforwarder"
SPLUNK_USER="splunkfwd"
SPLUNK_GROUP="splunkfwd"
DEPLOYMENT_SERVER="splunk-deploy.example.com:8089"

DEB_PACKAGE="latest-splunkforwarder.deb"
RPM_PACKAGE="latest-splunkforwarder.rpm"
LOG_FILE="/tmp/splunkUF.install.log"

timestamp() {
  date "+%Y-%m-%d %H:%M:%S"
}

log() {
  local level="$1"
  local message="$2"
  echo "$(timestamp) - component=SplunkInstall, level=${level}, message=${message}" | tee -a ${LOG_FILE}
}

log "INFO" "Starting Splunk Universal Forwarder installation script."

# Cleanup existing systemd unit if necessary
if [ -f /etc/systemd/system/SplunkForwarder.service ]; then
  log "INFO" "Removing existing SplunkForwarder systemd unit file."
  sudo "${SPLUNK_HOME}/bin/splunk" disable boot-start --accept-license --no-prompt || sudo rm -f /etc/systemd/system/SplunkForwarder.service
  sudo systemctl daemon-reexec
  sudo systemctl daemon-reload
fi

# Detect OS and install appropriate package
if [ -f /etc/debian_version ]; then
  log "INFO" "Detected Debian/Ubuntu system."
  if ! dpkg -i "$DEB_PACKAGE"; then
    log "ERROR" "Failed to install DEB package."
    exit 1
  fi
elif [ -f /etc/redhat-release ] || [ -f /etc/centos-release ] || grep -q "Amazon Linux" /etc/os-release 2>/dev/null; then
  log "INFO" "Detected RedHat/CentOS/Amazon Linux system."
  if ! rpm -i "$RPM_PACKAGE"; then
    log "ERROR" "Failed to install RPM package."
    exit 1
  fi
else
  log "ERROR" "Unsupported or unknown Linux distribution."
  exit 1
fi

# Set ownership
log "INFO" "Setting ownership of SPLUNK_HOME to ${SPLUNK_USER}:${SPLUNK_GROUP}."
sudo chown -R "${SPLUNK_USER}:${SPLUNK_GROUP}" "$SPLUNK_HOME"

# Configure deployment client
log "INFO" "Configuring deployment server."
sudo bash -c "cat > ${SPLUNK_HOME}/etc/system/local/deploymentclient.conf <<EOF
[deployment-client]
[target-broker:deploymentServer]
targetUri = ${DEPLOYMENT_SERVER}
EOF"

# Reset ownership after writing config
sudo chown -R "${SPLUNK_USER}:${SPLUNK_GROUP}" "$SPLUNK_HOME"

# First-time start (initializes internal folders)
log "INFO" "Starting Splunk once as ${SPLUNK_USER} to initialize."
sudo -u "$SPLUNK_USER" "${SPLUNK_HOME}/bin/splunk" start --accept-license --no-prompt

# Stop before enabling boot-start
log "INFO" "Stopping Splunk to prepare for boot-start enable."
sudo -u "$SPLUNK_USER" "${SPLUNK_HOME}/bin/splunk" stop

# Enable boot-start
log "INFO" "Enabling boot-start for SplunkForwarder under user ${SPLUNK_USER}."
sudo "${SPLUNK_HOME}/bin/splunk" enable boot-start -user "$SPLUNK_USER" --accept-license --no-prompt

# Start via systemd (no prompts on reboot)
log "INFO" "Starting SplunkForwarder via systemctl."
sudo systemctl daemon-reload
sudo systemctl start SplunkForwarder

log "INFO" "Splunk Universal Forwarder installation and setup completed successfully."
