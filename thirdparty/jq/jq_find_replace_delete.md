- Data sample: [Link](../../sampleData/raw/json/sample_array.json)


## Find and Replace based on select condition. Use `\=` for assignment
```
cat sample_array.json | jq '.[]| select (.host == "${MY_HOST_EUROPE}")| .details.country |= "xxxxxx" '
```
