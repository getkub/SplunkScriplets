## Steps

- Server
```
appName="DA_dropdown"
cp -pr /opt/splunk/etc/apps/$appName /tmp/ && tar -czf /tmp/${appName}.tgz -C /tmp/ ${appName} && chmod 777 /tmp/${appName}.tgz
```


- Client
```
appName="DA_dropdown"
destDir="docs/da"
fname="${destDir}/${appName}.tgz"

scp myuser@Server:/tmp/${appName}.tgz $fname
tar -xzf $fname -C $destDir  && rm $fname
```


## Dashboard Studio link within Splunk
```
/app/splunk-dashboard-studio
```