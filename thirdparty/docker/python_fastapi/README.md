## Build
```
myimage="python_fastapi"
myversion="v1.01"
mycontainer="python_fastapi"
docker build -t ${myimage}:${myversion} .
docker images
```

## Run
```
docker run --name $mycontainer -p 80:80 ${myimage}:${myversion}

http://localhost
http://localhost/docs
http://localhost/items/1?q=apple
```

## Clean-up
```
docker rm $(docker ps -qa -f status=exited)
docker rmi -f ${myimage}:${myversion}
```