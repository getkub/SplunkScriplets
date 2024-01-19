## find command with exec


- To print filename alongside cksum
```
find /path/to/search -name "*.txt" -exec sh -c 'echo "File: {}"; cksum {}' \;

find /path/to/search -name "*.txt" -exec sh -c 'for file do echo "File: $file"; cksum "$file"; done' sh {} +

```