#/etc/rsyslog.d/mycustom.conf
$template GenericTemplate, /var/log/syslog/%syslogfacility-text%-515/%FromHost%/messages.log
# $template SNMPTemplate, "/var/log/syslog/snmp/%FromHost%/messages.log"
$FileOwner splunk
$FileGroup splunk
$DirOwner splunk
$DirGroup splunk
#
local2.notice   ?GenericTemplate
#
# Custom Port
$template myCustomNetworkDevice, "/var/log/syslog/myCustomNetworkDevice/%FromHost%/messages.log"
$template PlainFormat,"%rawmsg%\n"
$RuleSet myCustomNetworkDeviceRule

# myCustomNetworkDeviceRule Ruleset
$InputTCPServerBindRuleset myCustomNetworkDevice
$InputTCPServerRun 20054

# EOF
