eg of extracting one stanza  (approximately)
```
/opt/splunk/bin/splunk cmd btool savedsearches list | sed -n -e '/^\[DMC Alert - Near Critical Disk Usage/,/^\[/p' | sed '$ d'
```
