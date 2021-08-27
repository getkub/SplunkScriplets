### kill a process
```
process='kubectl proxy'
kill `ps -ef | grep ${process}| grep -v grep| tr -s " " | cut -d ' ' -f2`
```
