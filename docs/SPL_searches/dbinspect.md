### dbinspect Examples

```
#Mainly related to indexes

# https://answers.splunk.com/answers/43417/search-to-provide-days-in-hot-warmdb.html
# |dbinspect index=name_of_your_index state=warm
|dbinspect index=main|convert timeformat=""%m/%d/%Y:%H:%M:%S"" mktime(earliestTime) as earliestTime|convert timeformat=""%m/%d/%Y:%H:%M:%S"" mktime(latestTime) as latestTime|stats min(earliestTime) as earliestTime max(latestTime) as latestTime sum(sizeOnDiskMB) as sizeOnDiskMB dc(path) as NumberOfBuckets by state|eval diff_seconds=(latestTime-earliestTime)/3600|eval earliestTime=strftime(earliestTime,"%m/%d/%Y:%H:%M:%S")|eval latestTime=strftime(latestTime,"%m/%d/%Y:%H:%M:%S")
```
