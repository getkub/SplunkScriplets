### macros savedsearches api Examples

```
#Actual searcxh
earliest=-10d index=mycompany_support sourcetype=some_sourcetype report_date=$report_date$
|table host,sourcetype

# to call as a macro
`mycompany_macro_some_os_aggregated_24h("2020-06-24")`
curl --silent -u ${user}:${pass} -k "https://${splunk_host}:9001/services/search/jobs/export" --data-urlencode search="search \`mycompany_macro_some_os_aggregated_24h(2020-06-24)\`" -d output_mode=${output_mode}


# To call as a savedsearch
# mycompany_ss_some_os_aggregated_24h
curl --silent -u ${user}:${pass} -k "https://${splunk_host}:9001/services/search/jobs/export" --data-urlencode search=" savedsearch  mycompany_ss_some_os_aggregated_24h" -d output_mode=${output_mode}
```
