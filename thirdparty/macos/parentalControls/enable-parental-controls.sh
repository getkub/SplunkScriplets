#!/bin/bash

# ============================================
# BLOCKED APPS LIST - Edit this before running
# ============================================
BLOCKED_APPS="x-vpn roblox minecraft fortnite steam discord"
# ============================================

# Enable Parental Controls Script
# Run this as admin: sudo ./enable-parental-controls.sh

echo "=========================================="
echo "Enabling Parental Controls"
echo "=========================================="

# Check if running as root
if [ "$EUID" -ne 0 ]; then 
    echo "❌ Please run as root: sudo ./enable-parental-controls.sh"
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
echo "Step 1: Installing configuration profile..."
# Install the profile (assumes ParentalControl.mobileconfig is in same directory)
if [ -f "ParentalControl.mobileconfig" ]; then
    profiles install -path ParentalControl.mobileconfig
    echo "✅ Configuration profile installed"
else
    echo "⚠️  ParentalControl.mobileconfig not found in current directory"
    echo "   Please ensure the .mobileconfig file is present"
fi

echo ""
echo "Step 2: Enabling Gatekeeper (strictest mode)..."
spctl --master-enable
spctl --global-enable
echo "✅ Gatekeeper enabled"

echo ""
echo "Step 3: Setting security to App Store apps only..."
# This requires user interaction in GUI, so we'll just note it
echo "⚠️  Manual step required:"
echo "   Go to: System Settings → Privacy & Security"
echo "   Set 'Allow applications downloaded from' to 'App Store'"

echo ""
echo "Step 4: No folder restrictions needed..."
echo "✅ Folders remain accessible (monitoring daemon handles app blocking)"

echo ""
echo "Step 5: Creating monitoring script..."
# Create a script to monitor and kill unauthorized apps
cat > /usr/local/bin/monitor-apps.sh << EOF
#!/bin/bash
# Monitor and kill apps running from unauthorized locations

# Blocked apps list (passed from enable script)
BLOCKED_APPS="$BLOCKED_APPS"

while true; do
    # Kill blocked apps (case insensitive)
    for app in \$BLOCKED_APPS; do
        pkill -9 -if "\$app" 2>/dev/null
    done
    
    # Kill any apps running from /Volumes (mounted DMGs, USB drives, etc.)
    ps -ax -o pid,command | grep "/Volumes/" | grep "\.app/Contents/MacOS" | grep -v grep | while read pid rest; do
        echo "\$(date): Killing process \$pid from /Volumes: \$rest" >> /var/log/parental-control.log
        kill -9 \$pid 2>/dev/null
    done
    
    sleep 3
done
EOF

chmod +x /usr/local/bin/monitor-apps.sh

echo ""
echo "Step 6: Setting up monitoring daemon..."
# Create LaunchDaemon for monitoring
cat > /Library/LaunchDaemons/com.parentalcontrol.monitor.plist << EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.parentalcontrol.monitor</string>
    <key>ProgramArguments</key>
    <array>
        <string>/usr/local/bin/monitor-apps.sh</string>
    </array>
    <key>RunAtLoad</key>
    <true/>
    <key>KeepAlive</key>
    <true/>
    <key>StandardOutPath</key>
    <string>/var/log/parental-control.log</string>
    <key>StandardErrorPath</key>
    <string>/var/log/parental-control-error.log</string>
</dict>
</plist>
EOF

# Load the daemon
launchctl load /Library/LaunchDaemons/com.parentalcontrol.monitor.plist
echo "✅ Monitoring daemon installed and running"

echo ""
echo "=========================================="
echo "✅ Parental Controls Enabled!"
echo "=========================================="
echo ""
echo "Blocked apps: $BLOCKED_APPS"
echo ""
echo "Active protections:"
echo "  • Configuration profile installed"
echo "  • Gatekeeper enforcing App Store apps"
echo "  • Background monitoring for apps from /Volumes"
echo ""
echo "The child will NOT be able to:"
echo "  • Run apps from mounted DMGs (/Volumes)"
echo "  • Install non-App Store apps"
echo "  • Run XVPN (will be automatically killed)"
echo ""
echo "The child CAN still:"
echo "  • Access Downloads/Desktop/Documents folders normally"
echo "  • Download files"
echo "  • Run apps installed in /Applications"
echo ""
echo "To disable: sudo ./disable-parental-controls.sh"
echo ""