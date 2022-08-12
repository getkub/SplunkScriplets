- Data sample: [Link](../../sampleData/raw/json/sample_array.json)
- https://lzone.de/cheat-sheet/jq

### Find and Replace based on select condition. Use `\=` for assignment
```
cat sample_array.json | jq '.[]| select (.host == "${MY_HOST_EUROPE}")| .details.country |= "xxxxxx" '
```

### Find and Replace based and retain entire data
```
jq 'map(if (.host == "${MY_HOST_EUROPE}") then .details.country = "xxxxxx" else . end )' sample_array.json
```

### Delete a key-value
```
cat sample_array.json | jq '.[]| select (.host == "${MY_HOST_EUROPE}")| del(.details.country)'
```
