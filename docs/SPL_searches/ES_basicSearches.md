### Enterprise Security Basic Searches

```
|inputlookup append=T access_tracker | search user=xyz | `get_asset(dest)`
|inputlookup append=T access_tracker | search user=xyz | `get_identity4events(user)`
|`inactive_account_usage("30","600")`| `settags("access")`| `ctime(lastTime)`| fields + user,inactiveDays
``` 