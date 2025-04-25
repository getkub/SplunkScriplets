### tstats searches Examples

```
# Find hosts which wer coming before but stopped logging (sliding scale)
| tstats count WHERE index=* earliest=-3d latest=-2d NOT [| tstats count WHERE index=* earliest=-2d latest=-1d BY host | fields host,source] BY host | lookup dnslookup clientip as host OUTPUT clienthost as DST_RESOLVED
```
