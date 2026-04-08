## MCP connecitivity test

```
## List tools
curl -k -X POST "https://myorg.api.scs.splunk.co/myorg/mcp/v1/ \
-H "Authorization: Bearer $SPLUNK_MCP_TOKEN" \
-H "Splunk-Endpoint: https://instance1.myorg.splunkcloud.com" \
-H "Content-Type: application/json"
-H "Accept: application/jon, text/event-stream" \
-d '{"jsonrpc": "2.0", "id": 2, "method": "tools/list"}'

```
