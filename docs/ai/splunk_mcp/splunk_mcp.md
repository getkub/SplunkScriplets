## Using CURL

```
export myip="192.168.31.175"
export splunk_mcp_token='xxxxxx'
https://${myip}$:8089/services/mcp
```

## Simple Search
```bash
curl -k -X POST "https://${myip}:8089/services/mcp" \
  -H "Authorization: Bearer $splunk_mcp_token" \
  -H "Content-Type: application/json" \
  -d '{
      "jsonrpc": "2.0",
      "id": 1768388416,
      "method": "tools/call",
      "params": {
        "name": "run_splunk_query",
        "arguments": {
          "query": "index=_internal | head 5 | stats count by host",
          "earliest": "-24h",
          "latest": "now"
        }
      }
    }'
```
## To query all tools
```bash
curl -k -X POST "https://${myip}:8089/services/mcp" \
  -H "Authorization: Bearer $splunk_mcp_token" \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "id": '$(date +%s)',
    "method": "tools/call",
    "params": {
      "name": "get_splunk_info",
      "arguments": {}
    }
  }'

```


## n8n config for HTTP client
```
{{ 
JSON.stringify({
  "jsonrpc": "2.0",
  "id": Math.floor(Date.now() / 1000),
  "method": "tools/call",
  "params": {
    "name": $json.tool || "get_splunk_info",
    "arguments": $json.args || {}
  }
}) 
}}
```