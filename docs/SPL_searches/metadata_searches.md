### metadata searches Examples

```
# source after uploading a csv
| inputlookup myfile.csv | join type=left [| metadata type=sources index=my_index | rex field=source "\/(?<ip>[0-9\.]+)\/[a-z\.]\.log*] | eventstats max(lastTime) as latestSource | where lastTime=latestSource| fields source,ip, lastTime] | eval lastTime=strfTime(lastTime,"%F-%T")
```
