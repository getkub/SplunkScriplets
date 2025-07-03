## Usage

```
export FILE_PATH="/path/to/your/file.conf"       # Can be macro.conf or savedsearch.conf
export LOOKUP_CSV="/path/to/lookup.csv"          # CSV file to upload
export APP_NAME="myapp"                          # Splunk app name
export SPLUNK_TOKEN="YOUR_TOKEN"                 # Bearer token for auth
export SPLUNK_URL="https://splunk.yourorg.com:8089"  # Splunk Management URL
USE_CERT="--use-cert"
```

- Macros
```
# Dry run (no actual changes)
python splunk_config_interface.py macro \
  --file-path "${FILE_PATH}" \
  --app "${APP_NAME}" \
  --dry-run \
  --log-level DEBUG \
  --token "${SPLUNK_TOKEN}" \
  --base-url "${SPLUNK_URL}" ${USE_CERT}

# Update macros
python splunk_config_interface.py macro \
  --file-path "${FILE_PATH}" \
  --app "${APP_NAME}" \
  --action-flag update \
  --log-level DEBUG \
  --token "${SPLUNK_TOKEN}" \
  --base-url "${SPLUNK_URL}" ${USE_CERT}

# Delete macros
python splunk_config_interface.py macro \
  --file-path "${FILE_PATH}" \
  --app "${APP_NAME}" \
  --action-flag delete \
  --log-level DEBUG \
  --token "${SPLUNK_TOKEN}" \
  --base-url "${SPLUNK_URL}" ${USE_CERT}


```

- SavedSearches
```
# Dry run
python splunk_config_interface.py savedsearch \
  --file-path "${FILE_PATH}" \
  --app "${APP_NAME}" \
  --dry-run \
  --log-level DEBUG \
  --token "${SPLUNK_TOKEN}" \
  --base-url "${SPLUNK_URL}" ${USE_CERT}

# Update saved searches
python splunk_config_interface.py savedsearch \
  --file-path "${FILE_PATH}" \
  --app "${APP_NAME}" \
  --action-flag update \
  --log-level DEBUG \
  --token "${SPLUNK_TOKEN}" \
  --base-url "${SPLUNK_URL}" ${USE_CERT}

# Delete saved searches
python splunk_config_interface.py savedsearch \
  --file-path "${FILE_PATH}" \
  --app "${APP_NAME}" \
  --action-flag delete \
  --log-level DEBUG \
  --token "${SPLUNK_TOKEN}" \
  --base-url "${SPLUNK_URL}" ${USE_CERT}

```

- CSV upload

```
# Upload CSV to Splunk Lookup
python ./scripts/upload_csv.py \
  --file-path "${LOOKUP_CSV}" \
  --app "${APP_NAME}" \
  --token "${SPLUNK_TOKEN}" \
  --base-url "${SPLUNK_URL}" \
  --log-level DEBUG ${USE_CERT}
```