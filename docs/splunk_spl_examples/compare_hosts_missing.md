## If hosts are missing compared to a CSV file
```
| inputlookup critical_hosts_file.csv
| eval host=upper(host)
| fields host threshold
| dedup host
| join type=left host [
    | tstats count where index=* earliest=-1h latest=-30m by host
    | eval host=upper(host)
    | rename count as actual_count
]
| eval status=case(
    isnull(actual_count), "MISSING",
    actual_count < threshold, "BELOW_THRESHOLD",
    true(), "OK"
)
| table host actual_count threshold status
```

### CSV file
```
host,threshold,timeSlot
host1,10,60
host2,20,60
```


## Hosts and sourcetype combination

```
| inputlookup my_reference.csv
| eval os_category = case(
    match(os_version, "Amazon Linux|CentOS|RHEL|Kali|Linux|Ubuntu|SLES"), "Linux",
    match(os_version, "Big Sur|Monterey|Sequoia|Ventura"), "MacOS",
    match(os_version, "Windows"), "Windows",
    true(), "Other"
)
| eval nt_host=upper(host)
| rex field=nt_host "(?P<host>^[^\.]+)"
| rename host as asset_host
| table os_category, nt_host, asset_host
| join type=left asset_host [
    | inputlookup logging_hosts_sourcetypes.csv
    | eval host=upper(host)
    | rename host as asset_host
    | stats values(sourcetype) as present_sourcetypes by asset_host
]
| eval expected_sourcetypes = case(
    os_category=="Linux", "syslog|auditd",
    os_category=="Windows", "WinEventLog",
    true(), ""
)
| eval expected_mv = split(expected_sourcetypes, "|")
| mvexpand expected_mv
| eval isLogging = if(isnull(mvfind(present_sourcetypes, expected_mv)) OR mvfind(present_sourcetypes, expected_mv) < 0, "no", "yes")
| table os_category, nt_host, asset_host, present_sourcetypes, missing_sourcetypes, isLogging
| stats count by isLogging
| eventstats sum(count) as total
| eval percent=round((count/total)*100, 2)
| table isLogging, percent
```
