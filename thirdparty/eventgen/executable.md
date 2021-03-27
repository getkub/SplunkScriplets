https://community.splunk.com/t5/Archive/generate-dummy-data-eventgen/m-p/454849
https://splunkbase.splunk.com/app/1924/

```
cp -r SA-Eventgen/lib/splunk_eventgen /tmp/
cp -r SA-Eventgen/lib/markupsafe /tmp/splunk_eventgen/lib/
cp -r SA-Eventgen/lib/jinja2 /tmp/splunk_eventgen/lib/
```

```
cp /tmp/splunk_eventgen/README/eventgen.conf.tutorial1 /tmp/splunk_eventgen/README/mytest.tutorial
```


```
cd /tmp/splunk_eventgen 
/opt/splunk/bin/splunk cmd python __main_.py generate README/mytest.tutorial
```
