## Once ESS version is enabled, disabling requires curl 

```
curl -k -u <USER:PASSWORD> \
    https://<STACK_URL>:8089/servicesNS/nobody/SA-ContentVersioning/properties/feature_flags/general \
    -X POST \
    -d versioning_init="0" \
    -d versioning_activated="0"
```
