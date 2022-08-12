- Data sample: [Link](../../sampleData/raw/json/sample_array.json)
- https://lzone.de/cheat-sheet/jq

### Find and Replace based on select condition. Use `\=` for assignment
```
cat sample_array.json | jq '.[]| select (.host == "${MY_HOST_EUROPE}")| .details.country |= "xxxxxx" '
```


### Delete a key-value
```
cat sample_array.json | jq '.[]| select (.host == "${MY_HOST_EUROPE}")| del(.details.country)'
```
