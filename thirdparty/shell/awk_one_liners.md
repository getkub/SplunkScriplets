- https://www.baeldung.com/linux/find-matching-text-replace-next-line
- Data sample: [Link](../../sampleData/raw/json/sample_array.json)

### Position based data manipulation
```
awk '/MY_HOST_EUROPE/{ rl = NR + 3 } NR == rl { gsub( /US/,"UK")} 3' sample1.json
```
