# Splunk Scripted Input – Secure API Collector

This scripted input securely pulls data from an external API using credentials stored in Splunk's internal password store (`storage/passwords`), with support for modular config via shell arguments.

---

## How to Add Credential

Run this once to store the API key securely in Splunk:

```bash
curl -k -u admin:changeme \
  https://localhost:8089/servicesNS/nobody/my_scripted_inputs/storage/passwords \
  -d name=https://api.example.com \
  -d username=api_user \
  -d password=real_api_key_here
```

---

## How It Works

- `run_api_collector.sh` runs every N seconds (configured in `inputs.conf`)
- It calls `api_collector.py` with arguments:
  - `--app`: Splunk app name
  - `--user`: Username for credential
  - `--realm`: Credential realm (API base URL)
  - `--endpoint`: Actual API endpoint to call
- The Python script fetches the password securely using the session key passed via `passAuth = splunk-system-user`

---

## How to Run (Script Entry Point)

```bash
#!/bin/bash

APP_NAME="my_scripted_inputs"
USERNAME="api_user"
REALM="https://api.example.com"
API_ENDPOINT="https://api.example.com/data"

$SPLUNK_HOME/bin/splunk cmd python \
  $SPLUNK_HOME/etc/apps/$APP_NAME/bin/api_collector.py \
  --app "$APP_NAME" \
  --user "$USERNAME" \
  --realm "$REALM" \
  --endpoint "$API_ENDPOINT"
```

Make sure `run_api_collector.sh` is referenced in `inputs.conf`:

```ini
[script://./bin/run_api_collector.sh]
disabled = 0
interval = 300
sourcetype = api_collector
index = main
passAuth = splunk-system-user
```

---
