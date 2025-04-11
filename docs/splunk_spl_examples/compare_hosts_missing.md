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
