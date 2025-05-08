## Various Insert into the system

@app =  myapp
@owner = nobody
@endpoint = saved/searches

## Basic
POST {{baseUrl}}/services/search/jobs?output_mode=json
Authorization: Bearer {{token}}
Content-Type: application/x-www-form-urlencoded


## Insert with alerts/report
POST {{baseUrl}}/servicesNS/{{owner}}/{{app}}/{{endpoint}}
Authorization: Bearer {{token}}
Content-Type: application/x-www-form-urlencoded

name=TEST_API_Search
&search=search index=_audit | stats count
&dispatch.earliest_time=-5m
&dispatch.latest_time=now
&description=Created via REST API
&disabled=0
&cron_schedule=*/3 * * * *
&is_scheduled=1


## Update existing
POST {{baseUrl}}/servicesNS/{{owner}}/{{app}}/saved/searches/TEST_API_Search
Authorization: Bearer {{token}}
Content-Type: application/x-www-form-urlencoded

search=search index=_audit | stats count
&dispatch.earliest_time=-10m
&cron_schedule=*/5 * * * *
&description=Updated via API
