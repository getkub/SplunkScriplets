
## How to Add Credential to Splunk
- Run this once, from CLI or API:

```
curl -k -u admin:changeme \
  https://localhost:8089/servicesNS/nobody/my_scripted_inputs/storage/passwords \
  -d name=https://api.example.com \
  -d username=api_user \
  -d password=real_api_key_here
```