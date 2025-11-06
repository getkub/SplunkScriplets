#!/bin/bash

# Disable Parental Controls Script
# Run this as admin: sudo ./disable-parental-controls.sh

echo "=========================================="
echo "Disabling Parental Controls"
echo "=========================================="

# Check if running as root
if [ "$EUID" -ne 0 ]; then 
    echo "❌ Please run as root: sudo ./disable-parental-controls.sh"
    exit 1
fi

# Get the child's username
read -p "Enter the child's username: " CHILD_USER

# Verify user exists
if ! id "$CHILD_USER" &>/dev/null; then
    echo "❌ User $CHILD_USER does not exist"
    exit 1
fi

echo ""
echo "Step 1: Removing configuration profile..."
# Find and remove the profile
PROFILE_ID="com.parentalcontrol.profile"
if profiles show | grep -q "$PROFILE_ID"; then
    profiles remove -identifier "$PROFILE_ID"
    echo "✅ Configuration profile removed"
else
    echo "⚠️  Configuration profile not found (may already be removed)"
fi

echo ""
echo "Step 2: Stopping monitoring daemon..."
# Unload and remove the LaunchDaemon
if [ -f /Library/LaunchDaemons/com.parentalcontrol.monitor.plist ]; then
    launchctl unload /Library/LaunchDaemons/com.parentalcontrol.monitor.plist 2>/dev/null
    rm /Library/LaunchDaemons/com.parentalcontrol.monitor.plist
    echo "✅ Monitoring daemon stopped and removed"
else
    echo "⚠️  Monitoring daemon not found"
fi

echo ""
echo "Step 3: Removing monitoring script..."
if [ -f /usr/local/bin/monitor-apps.sh ]; then
    rm /usr/local/bin/monitor-apps.sh
    echo "✅ Monitoring script removed"
else
    echo "⚠️  Monitoring script not found"
fi

echo ""
echo "Step 4: No folder permissions to restore..."
echo "✅ Folders were not modified"

echo ""
echo "Step 5: Gatekeeper settings..."
echo "⚠️  Note: Gatekeeper is still enabled (recommended for security)"
echo "   If you want to disable it (NOT recommended):"
echo "   Run: sudo spctl --master-disable"

echo ""
echo "Step 6: Cleaning up logs..."
rm -f /var/log/parental-control.log 2>/dev/null
rm -f /var/log/parental-control-error.log 2>/dev/null
echo "✅ Logs cleaned"

echo ""
echo "=========================================="
echo "✅ Parental Controls Disabled!"
echo "=========================================="
echo ""
echo "All restrictions have been removed."
echo "The user '$CHILD_USER' now has standard user permissions."
echo ""
echo "To re-enable: sudo ./enable-parental-controls.sh"
echo ""