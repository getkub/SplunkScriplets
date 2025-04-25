### distributed system tricks Examples

```
# Query a lookup from a joined up search head to another SH using rest
# https://www.splunk.com/blog/2017/06/08/syncing-lookups-using-pure-spl.html

| rest splunk_server=sh1 /services/search/jobs/export search="| inputlookup demo_assets.csv" output_mode=csv | fields value
```
