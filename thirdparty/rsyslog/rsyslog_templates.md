## Quality templates

https://www.rsyslog.com/doc/v8-stable/configuration/templates.html

```
template(name="RSYSLOG_StdJSONFmt" type="string"
     string="{\"message\":\"%msg:::json%\",\"fromhost\":\"%HOSTNAME:::json%\",\"facility\":
             \"%syslogfacility-text%\",\"priority\":\"%syslogpriority-text%\",\"timereported\":
             \"%timereported:::date-rfc3339%\",\"timegenerated\":
             \"%timegenerated:::date-rfc3339%\"}")
```