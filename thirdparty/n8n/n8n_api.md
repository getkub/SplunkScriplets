## n8n API useful commands

## API playground

- http://localhost:5678/api/v1/docs/#/Execution/get_executions__id_

### Retrieve specific execution
```
id=72
curl -X GET "http://localhost:5678/api/v1/executions/${id}?includeData=true" \
  -H 'accept: application/json' \
  -H "X-N8N-API-KEY: ${n8n_api_key}"
```


### Delete specific execution

```
id=72
curl -X DELETE "http://localhost:5678/api/v1/executions/${id}" \
  -H 'accept: application/json' \
  -H "X-N8N-API-KEY: ${n8n_api_key}"

## for multiple
for id in {10..60}
do
  echo "execution ID: $id"

  curl -X DELETE "http://localhost:5678/api/v1/executions/${id}" \
  -H 'accept: application/json' \
  -H "X-N8N-API-KEY: ${n8n_api_key}"
done
```
