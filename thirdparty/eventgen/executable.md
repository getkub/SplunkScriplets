# Run eventgen without Splunk

### Copy ONLY relevant parts to a temporary location


#### if its from Splunk App
```
tempLocation="/tmp/ev_code"
mkdir -p $tempLocation
eventGenDir="/opt/splunk/etc/apps/SA-Eventgen"
cp -r ${eventGenDir}/lib/splunk_eventgen ${tempLocation}
cp -r ${eventGenDir}/lib/splunk_eventgen/__main__.py ${tempLocation}
cp -r ${eventGenDir}/bin/markupsafe ${tempLocation}/splunk_eventgen/lib/
cp -r ${eventGenDir}/bin/jinja2 ${tempLocation}/splunk_eventgen/lib/
```

#### if its from source-code
```
tempLocation="/tmp/ev_src2"
mkdir -p $tempLocation
eventGenDir="/tmp/eventgen-7.2.1"
cp -r ${eventGenDir}/splunk_eventgen ${tempLocation}
cp -r ${tempLocation}/splunk_eventgen/__main__.py ${tempLocation}
```

```
cd ${tempLocation}/splunk_eventgen 
/opt/splunk/bin/splunk cmd python __main__.py generate splunk_eventgen/README/eventgen.conf.tutorial2

# OR
python3 __main__.py generate splunk_eventgen/README/eventgen.conf.tutorial2

# depending on the conf, it will be created. Above example will create in /tmp/ciscosample.log
```
