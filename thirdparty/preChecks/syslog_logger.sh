# syslog simulation using logger or netcat (nc)
remoteIP="10.12.13.14"
remotePort="514"
sampleMessage="TEST_MSG"

# logger -n $remoteIP -P $remotePort $sampleMessage

echo $sampleMessage | nc $remoteIP $remotePort
