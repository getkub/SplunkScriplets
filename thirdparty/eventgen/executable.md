https://community.splunk.com/t5/Archive/generate-dummy-data-eventgen/m-p/454849

https://splunkbase.splunk.com/app/1924/

### Copy ONLY relevant parts to a temporary location
```
tempLocation="/tmp"
cp -r SA-Eventgen/lib/splunk_eventgen ${tempLocation}
cp -r SA-Eventgen/lib/markupsafe ${tempLocation}/splunk_eventgen/lib/
cp -r SA-Eventgen/lib/jinja2 ${tempLocation}/splunk_eventgen/lib/
```

```
cp ${tempLocation}/splunk_eventgen/README/eventgen.conf.tutorial1 ${tempLocation}/splunk_eventgen/README/mytest.tutorial
```


```
cd ${tempLocation}/splunk_eventgen 
/opt/splunk/bin/splunk cmd python __main_.py generate README/mytest.tutorial
```
