## Build & Push using docker to the repository
```
docker_image="server:1235/image_name:tag_id"
docker build --no-cache  -t ${docker_image} .
docker push ${docker_image}
```

## Running a docker image
```
pod_name="my_pod_name"
work_dir="/opt/myapp"
https_proxy="http://10.134.256.23:5600"
docker_image="server:1235/image_name:tag_id"
script_and_params="cat /tmp/myfile"

docker run --rm -it --name ${pod_name}  -w $work_dir -e https_proxy=${https_proxy} $docker_image python ${script_and_params}
```

## Running the above in k8s
#### DockerFile is important and to ensure all proxy settings etc are done
```
k8s_namespace="my_k8s_ns"
pod_name="my_pod_name"
k8s_image="server:1235/image_name:tag_id"
script_and_params="cat /tmp/myfile"
kubectl -n $k8s_namespace run -i --attach $pod_name="my_pod_name" --image=${k8s_image} ${script_and_params}

## Clean-up
kubectl -n $k8s_namespace delete pod $pod_name
```
