### Tricky Splunk Searches

#### Dynamic Variables in Searches
```
| gentimes start=-1 | eval myVar=stuff | map search="| dbquery source \"select * from tble where timestamp >= $myVar$ \" "
```

#### Dynamic Time Values
```
index=someData [noop|stats count|fields|eval earliest=relative_time(now(),"@d+10h")|eval latest=relative_time(now(),"@d+21h")| convert timeformat="%m/%d/%Y:%T" ctime(*)| format "" "" "" "" "" ""]
``` 