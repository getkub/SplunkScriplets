### datamodels.searches Examples

```
# View Datamodel Acceleration graphs

| `datamodel("Splunk_Audit", "Datamodel_Acceleration")` | `drop_dm_object_name("Datamodel_Acceleration")` | join type=outer last_sid [| rest splunk_server=* count=0 /services/search/jobs reportSearch=summarize* | rename sid as last_sid | fields last_sid,runDuration] | eval size(MB)=round(size/1048576,1) | eval retention(days)=retention/86400 | eval complete(%)=round(complete*100,1) | eval runDuration(s)=round(runDuration,1) |  sort 100 + datamodel | fieldformat earliest=strftime(earliest, "%m/%d/%Y %H:%M:%S") | fieldformat latest=strftime(latest, "%m/%d/%Y %H:%M:%S") | fields datamodel,app,cron,retention(days),earliest,latest,is_inprogress,complete(%),size(MB),runDuration(s),last_error


# With no acceleration
|datamodel Network_Traffic All_Traffic search | search sourcetype="cisco:asa" | stats count by All_Traffic.dest
```
