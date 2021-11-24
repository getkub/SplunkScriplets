### To filter per service and get last logs
https://unix.stackexchange.com/questions/422213/how-to-see-the-latest-x-lines-from-systemctl-service-log
```
journalctl --unit=my.service -n 100 --no-pager
journalctl -u <service name> -n <number of lines> -f
journalctl -u SERVICE_NAME -e
journalctl --unit=my.service --since "1 hour ago" -p err


# slow
journalctl --unit=my.service | tail -n 300
journalctl --unit=my.service | sed -e :a -e '$q;N;301,$D;ba' 

```
