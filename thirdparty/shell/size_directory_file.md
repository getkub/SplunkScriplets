## Find size of largest file and format it

```
sudo su -
find /opt -type f -exec du -h {} + | sort -rh | head -20
```
