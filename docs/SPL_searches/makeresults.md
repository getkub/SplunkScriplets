### makeresults Examples

```
# to split data to multiple events 

| makeresults | eval _raw="08.02.2017 08:20:36.618 | 1752 | INFO | 10098094 | GW: session(90200371) status = INITIALIZING.;
08.02.2017 08:20:36.618 | 1752 | INFO | 10098094 | GW: session(90200371) status = pending_app_gw.;
08.02.2017 08:20:36.706 | 5344 | INFO | 10098094 | GW: session(90200371) status = ACTIVE.;"|
rex max_match=0 field=_raw "(?<perLine>[^;]+)" | mvexpand perLine | table perLine|rex field=perLine "^[^(\n]*((?P\d+)"
```
