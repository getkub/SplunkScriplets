#!/bin/bash

# ============================================================================
# Splunk Universal Forwarder Installation Script for Linux
# Version: 1.2
#
# Description:
# This script installs and configures the Splunk Universal Forwarder (UF) 
# on supported Linux systems (Debian/Ubuntu, RedHat/CentOS, Amazon Linux).
#
# Key Features:
# - Detects OS and installs appropriate package (DEB/RPM)
# - Creates and sets correct ownership to a dedicated non-root user
# - Registers Splunk as a systemd service for automatic start on boot
# - Configures deployment server settings
# - Starts Splunk cleanly via systemd (no password prompt at boot)
#
# Notes:
# - Script must be run with sudo/root privileges
# - Splunk runs under the dedicated user specified in SPLUNK_USER
# - Admin user creation (user-seed.conf) is intentionally skipped
#
# ============================================================================
# Configuration Variables
SPLUNK_HOME="/opt/splunkforwarder"
SPLUNK_USER="splunkfwd"
SPLUNK_GROUP="splunkfwd"
DEPLOYMENT_SERVER="splunk-deploy.example.com:8089"

DEB_PACKAGE="latest-splunkforwarder.deb"
RPM_PACKAGE="latest-splunkforwarder.rpm"

timestamp() {
  date "+%Y-%m-%d %H:%M:%S"
}

log() {
  local level="$1"
  local message="$2"
  echo "$(timestamp) - component=SplunkInstall, level=${level}, message=${message}"
}

log "INFO" "Starting Splunk Universal Forwarder installation script."

# Cleanup previous systemd service if needed
if [ -f /etc/systemd/system/SplunkForwarder.service ]; then
  log "INFO" "Removing existing SplunkForwarder systemd unit file."
  sudo "${SPLUNK_HOME}/bin/splunk" disable boot-start --accept-license --no-prompt || sudo rm -f /etc/systemd/system/SplunkForwarder.service
  sudo systemctl daemon-reexec
  sudo systemctl daemon-reload
fi

# Detect platform and install package
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

# Set initial ownership
log "INFO" "Setting ownership of SPLUNK_HOME to ${SPLUNK_USER}."
sudo chown -R "${SPLUNK_USER}:${SPLUNK_GROUP}" "$SPLUNK_HOME"

# Configure deployment client
log "INFO" "Configuring deployment server."
sudo bash -c "cat > ${SPLUNK_HOME}/etc/system/local/deploymentclient.conf <<EOF
[deployment-client]
[target-broker:deploymentServer]
targetUri = ${DEPLOYMENT_SERVER}
EOF"

# Re-set ownership after config change
sudo chown -R "${SPLUNK_USER}:${SPLUNK_GROUP}" "$SPLUNK_HOME"

# First-time start as non-root to initialize config
log "INFO" "First-time Splunk start as ${SPLUNK_USER} to initialize files."
sudo -u "$SPLUNK_USER" "${SPLUNK_HOME}/bin/splunk" start --accept-license --no-prompt

# Stop it before boot-enable
log "INFO" "Stopping Splunk before enabling boot-start."
sudo -u "$SPLUNK_USER" "${SPLUNK_HOME}/bin/splunk" stop

# Enable boot-start under non-root user
log "INFO" "Enabling Splunk to start at boot via systemd."
sudo "${SPLUNK_HOME}/bin/splunk" enable boot-start -user "$SPLUNK_USER" --accept-license --no-prompt

# Start via systemd (no prompts at reboot)
log "INFO" "Starting SplunkForwarder via systemctl."
sudo systemctl daemon-reload
sudo systemctl start SplunkForwarder

log "INFO" "Splunk Universal Forwarder installation and configuration completed successfully."
