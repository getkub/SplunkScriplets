# An example for rsyslog logrotate daemon config. 
# Written by isplunker.com
#/etc/logrotate.d/myrotate.conf
/var/log/syslog/*.log
/var/log/syslog/*/*.log
/var/log/syslog/*/*/*.log
/var/log/syslog/*/*/*/*.log
 {
   notifempty                 # Do not rotate the log if it is empty
   compress                   # Old versions of log files are compressed with gzip
   delaycompress              # Postpone compression of the previous log file to the next rotation cycle
   create 0600 splunk splunk  # How log file should be created
   hourly                     # Interval
   dateext                    # Archive old versions of log files adding a daily extension
   missingok                  # If the log file is missing, go on to the next one without issuing an error message
   rotate 10                  # keeps as many old logs
   size 500M                  # maximum size for your logs
   sharedscripts              # Safeguard against multiple runs
   postrotate                 # actions after completing rotate
   /bin/kill -HUP `cat /var/run/syslogd.pid 2>/dev/null` 2 >/dev/null || true endscript
 }
 