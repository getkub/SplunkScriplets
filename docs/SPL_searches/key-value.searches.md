### key-value.searches Examples

```
#https://answers.splunk.com/answers/523059/how-extract-fields-and-values-on-a-multivalue-fiel.html
Your Base Search Here
 | rex max_match=0 "\"(?<kvp>[^=\"]+=[^=\"]+)\""
 | table _time host kvp*
 | streamstats count AS serial
 | mvexpand kvp
 | rex field=kvp "^(?<kvp_key>[^=\"]+)=(?<kvp_value>[^=\"]+)$"
 | eval {kvp_key} = kvp_value
 | rename COMMENT AS "If you need to reconstitute original events, then add in the next line"
 | rename COMMENT AS "| fields - kvp* | stats values(_time) AS _time values(*) AS * BY serial"
 | table Name p_name Type status
```
