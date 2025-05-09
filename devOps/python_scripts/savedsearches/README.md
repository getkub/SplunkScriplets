## Splunk insert/update via API

- Step1: Ensure token is setup and updated into code
- Step2: Ensure the Splunk:8089 certificate chain is updated into files location
- Then run like below

### Default (dry-run)
```
python savedsearches/upsert.py
```

### Actually perform POST requests
```
python savedsearches/upsert.py --real-run
```