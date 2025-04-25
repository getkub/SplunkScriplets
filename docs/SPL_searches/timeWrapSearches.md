### timeWrapSearches Examples

```
# To compare two values continously
index=_internal earliest=-8d@d latest=-7d@d| eval ReportKey="1weekBefore"|  timechart span=10m count by ReportKey | append [index=_internal earliest=-2d@d latest=-1d@d| eval ReportKey="yesterday"|  timechart span=10m count by ReportKey]


# Faster
|tstats count where index=foo earliest=-2d@d latest=-1d@d by _time span=5m
| eval ReportKey="Baseline" | eval _time=_time+60*60*24
| append [|tstats count where index=foo earliest=-1d@d latest=0d@d by _time span=5m
| eval ReportKey="NewValue" ]
| timechart span=5m sum(count) by ReportKey
```
