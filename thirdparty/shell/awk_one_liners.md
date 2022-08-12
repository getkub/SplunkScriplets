sample1.json
- https://www.baeldung.com/linux/find-matching-text-replace-next-line
```
	[
	   {
	        "host": "${MY_HOST_AMERICAS}",
	        "port": 443,
	        "details": {
	            "country": "US",
	            "clientAuthEnabled": "false",
	            "enabled": "true"
	        }
	    },
	   {
	        "host": "${MY_HOST_EUROPE}",
	        "port": 443,
	        "details": {
	            "country": "UK",
	            "clientAuthEnabled": "false",
	            "enabled": "true"
	        }
	    },
	   {
	        "host": "${MY_HOST_EUROPE}",
	        "port": 443,
	        "details": {
	            "country": "US",
	            "clientAuthEnabled": "false",
	            "enabled": "true"
	        }
	    }
]


```

### Position based data manipulation
```
awk '/MY_HOST_EUROPE/{ rl = NR + 3 } NR == rl { gsub( /US/,"UK")} 3' sample1.json
```
