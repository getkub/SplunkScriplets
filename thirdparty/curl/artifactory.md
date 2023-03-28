## JFrog Artifactory

```
# PUT
curl -v -T $fname "${artifactory_url}/${directory}/${fname}" 
```



```
# DELETE
curl -v --request DELETE "${artifactory_url}/${directory}/${fname}" 
```
