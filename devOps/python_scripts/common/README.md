## Usage

- Macros
```
python splunk_config_interface.py macro --file-path /where/you/kept/macro.conf --app myapp --dry-run --log-level DEBUG
python splunk_config_interface.py macro --file-path /where/you/kept/macro.conf --app myapp --action-flag update --log-level DEBUG
python splunk_config_interface.py macro --file-path /where/you/kept/macro.conf --app myapp --action-flag delete --log-level DEBUG
```

- SavedSearches
```
python splunk_config_interface.py savedsearch --file-path /where/you/kept/savedsearch.conf --app myapp --dry-run --log-level DEBUG
python splunk_config_interface.py savedsearch --file-path /where/you/kept/savedsearch.conf --app myapp --action-flag update --log-level DEBUG
python splunk_config_interface.py savedsearch --file-path /where/you/kept/savedsearch.conf --app myapp --action-flag delete --log-level DEBUG
```

- CSV upload

```
python ./scripts/upload_csv.py \
  --file-path "${csv_path}" \
  --app "${appName}" \
  --token "${mytoken}" \
  --base-url "https://myorg.splunkcloud.com:8089" \
  --log-level DEBUG
```