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
