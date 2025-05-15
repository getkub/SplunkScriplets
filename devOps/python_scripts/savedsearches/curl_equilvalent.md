## Curl to insert savedsearches

```
curl -k -u user:pass https://sh1:8089/servicesNS/nobody/SplunkEnterpriseSecuritySuite/saved/searches \
  -H "Content-Type: application/x-www-form-urlencoded" \
  --data-urlencode "name=Threat - 3754818 API TEST - Rule" \
  --data-urlencode "search=index=_internal | stats count by sourcetype" \
  --data-urlencode "description=Threat - 3754818 API TEST - Rule" \
  --data-urlencode "disabled=false" \
  --data-urlencode "is_scheduled=true" \
  --data-urlencode "cron_schedule=*/3 * * * *" \
  --data-urlencode "dispatch.earliest_time=-24h" \
  --data-urlencode "dispatch.latest_time=now" \
  --data-urlencode "dispatch.rt_backfill=1" \
  --data-urlencode "alert.track=1" \
  --data-urlencode "alert.suppress=0" \
  --data-urlencode "request.ui_dispatch_app=SplunkEnterpriseSecuritySuite" \
  --data-urlencode "actions=notable" \
  --data-urlencode "action.notable=1" \
  --data-urlencode "action.notable.param.rule_title=Threat - 3754818 API TEST - Rule" \
  --data-urlencode "action.notable.param.rule_description=Threat - 3754818 API TEST - Rule" \
  --data-urlencode "action.notable.param.security_domain=threat" \
  --data-urlencode "action.notable.param.severity=high" \
  --data-urlencode "action.notable.param.investigation_type=default" \
  --data-urlencode "action.notable.param.verbose=0" \
  --data-urlencode "action.notable.param.drilldown_dashboards=[]" \
  --data-urlencode "action.notable.param.drilldown_searches=[]" \
  --data-urlencode "action.correlationsearch.detection_type=ebd" \
  --data-urlencode "action.correlationsearch.enabled=1" \
  --data-urlencode "action.correlationsearch.label=Threat - 3754818 API TEST - Rule" \
  --data-urlencode "action.analyzeioc.param.verbose=0" \
  --data-urlencode "action.customsearchbuilder.enabled=false" \
  --data-urlencode "action.keyindicator.invert=0" \
  --data-urlencode "action.makestreams.param.verbose=0" \
  --data-urlencode "action.nbtstat.param.verbose=0" \
  --data-urlencode "action.nslookup.param.verbose=0" \
  --data-urlencode "action.ping.param.verbose=0" \
  --data-urlencode "action.risk.forceCsvResults=1" \
  --data-urlencode "action.risk.param._risk=[{\"risk_object_field\":\"dest\",\"risk_object_type\":\"system\",\"risk_score\":1}]" \
  --data-urlencode "action.risk.param._risk_message=Threat - 3754818 API TEST - Rule" \
  --data-urlencode "action.risk.param.verbose=0" \
  --data-urlencode "action.send2uba.param.verbose=0" \
  --data-urlencode "action.threat_add.param.verbose=0" \
  --data-urlencode "action.webhook.enable_allowlist=0"
```
