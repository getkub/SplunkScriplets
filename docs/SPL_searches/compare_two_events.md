### compare two events Examples

```
#Compare two raw events side by side

(index=xyz) sourcetype=WinEventLog:Security ((Logon_Type=2 OR Logon_Type=10 OR Logon_Type=11 OR Logon_Type=3) ((EventCode=4624) OR EventCode=528)) user=someuser (host=*)
| head 1
| table _raw
| rename _raw as client_event
| eval item="aa"
| join item  [ search (index=xyz) sourcetype=WinEventLog:Security ((Logon_Type=2 OR Logon_Type=10 OR Logon_Type=11 OR Logon_Type=3) ((EventCode=4624) OR EventCode=528)) user=someuser (host=dc*)
| head 1
| table _raw
| rename _raw as dc_event
| eval item="aa"]
```
