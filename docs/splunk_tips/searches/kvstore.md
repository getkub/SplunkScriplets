### KVstore objects & Sizes
```
| rest /services/server/introspection/kvstore/collectionstats
| mvexpand data
| spath input=data
| rex field=ns "(?<App>.*)\.(?<Collection>.*)"
| eval dbsize=round(size/1024/1024, 2)
| eval indexsize=round(totalIndexSize/1024/1024, 2)
| stats first(count) AS "Objects" first(nindexes) AS Accelerations first(indexsize) AS "Acceleration_Size_MB" first(dbsize) AS "MongoDB_Collection_Size_MB" by App, Collection
| sort - Objects
| head 20
```