### incident impact Examples

```
#Data loss based on license usage
index=_internal source="*license_usage.log" type="Usage" earliest=-2h@h
| bucket span=1h h
| strcat h + ";" + st as key
| stats sum(b) as totalBytes  _time,key
| convert timeformat="%Y-%m-%d:%H:00" ctime(_time) as Date
| xyseries key Date KB
```
