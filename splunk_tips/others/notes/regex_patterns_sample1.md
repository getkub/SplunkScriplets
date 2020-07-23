```
2013-02-28 09:57:56,668 ERROR SomeCallLogger - ESS10005 Cpc portalservices: Exception caught while writing log messege to MEA Call:  {}
java.sql.SQLSyntaxErrorException: ORA-00942: table or view does not exist

	at oracle.jdbc.driver.T4CTTIoer.processError(T4CTTIoer.java:445)
	at oracle.jdbc.driver.T4CTTIoer.processError(T4CTTIoer.java:396)
```

GROK
```
\A%{TIMESTAMP_ISO8601:timestamp}\s+%{LOGLEVEL:loglevel}\s+(?<logger>(?:[a-zA-Z0-9-]+\.)*[A-Za-z0-9$]+)\s+(-\s+)?(?=(?<msgnr>[A-Z]+[0-9]{4,5}))*%{DATA:message}({({[^}]+},?\s*)*})?\s*$(?<stacktrace>(?m:.*))?
```
