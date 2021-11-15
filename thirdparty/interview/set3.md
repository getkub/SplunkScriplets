- Give an example of JSON to represent a data for for below scenario
```
IT Department -> 3 managers -> 1st manager have 2 reportees & 2nd manager have 3 reportees & 3rd manager don't have any reportees
```
- Convert the above example to a YAML notation
- How would your approach be to convert below data into a key-value pair (or meaningful dataset). This is a very common type of dataset you might have seen if you worked on Web-Application
```
83.149.9.216 - - [17/May/2015:10:05:03 +0000] "GET /presentations/logstash-monitorama-2013/images/retail-search.png HTTP/1.1" 200 203023 "http://semicomplete.com/presentations/logstash-monitorama-2013/" "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1700.77 Safari/537.36"
83.149.9.216 - - [17/May/2015:10:05:43 +0000] "GET /presentations/logstash-monitorama-2013/images/frontpage-dashboard3.png HTTP/1.1" 200 171717 "http://semicomplete.com/presentations/logstash-monitorama-2013/" "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1700.77 Safari/537.36"
```
- Regex: I've got a regex in the code as   `([^\s]+)\s+(\w)+$` CAn you please explain what it is trying to do? Any idea to write a GROK equivalent of it?
