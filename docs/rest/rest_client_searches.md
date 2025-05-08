## REST API client style searches

- List Saved Searches in an App (Filtered by App Name)

```
@appName = "my_app"

POST {{baseUrl}}/services/search/jobs?output_mode=json
Authorization: Bearer {{token}}
Content-Type: application/x-www-form-urlencoded

search=| rest /servicesNS/nobody/{{app}}/saved/searches 
       | table title, eai:acl.app, description
       | rename eai:acl.app AS app
       | search app="{{appName}}"
```

- Get Full Content of a Specific Saved Search

```
@search_name = "my_search"

POST {{baseUrl}}/services/search/jobs?output_mode=json
Authorization: Bearer {{token}}
Content-Type: application/x-www-form-urlencoded

search=| rest /servicesNS/nobody/{{app}}/saved/searches/{{search_name}}
       | table title, eai:acl.app, qualifiedSearch
       | rename eai:acl.app AS app

```