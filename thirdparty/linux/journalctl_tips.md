### To filter per service and get last logs
https://unix.stackexchange.com/questions/422213/how-to-see-the-latest-x-lines-from-systemctl-service-log
```
journalctl --unit=my.service -n 100 --no-pager
journalctl -u <service name> -n <number of lines> -f
journalctl -u SERVICE_NAME -e
journalctl --unit=my.service --since "1 hour ago" -p err

# To reverse 100 lines
journalctl -u <service name> -r -n 100


# slow
journalctl --unit=my.service | tail -n 300
journalctl --unit=my.service | sed -e :a -e '$q;N;301,$D;ba' 

```


## Time based filters
```
journalctl _UID=33 --since today
journalctl --since 09:00 --until "1 hour ago"
journalctl --since "2015-01-10 17:15:00"
journalctl --since "2015-01-10" --until "2015-01-11 03:00"
```


### Other tips
```
# group IDs the systemd journal has entries for
journalctl -F _GID

# entries that involve the bash executable
journalctl /usr/bin/bash

# messages from five boots ago
journalctl -k -b -5

# logged at the error level or above
journalctl -p err -b

# Formatting to json
journalctl -b -u nginx -o json
```
