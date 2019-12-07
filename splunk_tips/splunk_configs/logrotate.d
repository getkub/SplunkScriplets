#/etc/logrotate.d/myrotate.conf
/var/log/syslog/*/*/messages.log
 {
   notifempty
   nocompress
   create 0600 splunk splunk
   hourly
   dateext
   missingok
   rotate 1
   sharedscripts
   postrotate
   /bin/kill -HUP `cat /var/run/syslogd.pid 2>/dev/null` 2 >/dev/null || true endscript
 }
