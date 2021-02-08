# syslog simulation using logger
remoteIP="10.12.13.14"
remotePort="514"
sampleMessage="TEST_MSG"

logger -n $remoteIP -P $remotePort $sampleMessage
