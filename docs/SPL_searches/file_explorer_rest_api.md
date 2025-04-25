### file explorer rest api Examples

```
# To use Splunk REST endpoint for exploring filesystem

| REST splunk_server=local /services/apps/local
| fields title
| map maxsearches=1000 search="| REST splunk_server=local /services/admin/file-explorer/%252Fopt%252Fsplunk%252Fetc%252Fapps%252F$myapp$%252Flocal"
| fields title

```
