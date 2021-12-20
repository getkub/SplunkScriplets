### In case if you cannot access via kubectl
```
curl https://api.myip.com # To find current IP of GCP console
myns=xyz
myproj=some_project
myzone="europe-west1-b"

kubectl -n ${myns} get pods -o wide
mynode="fill_up_node_from_above"

# GET access to the node
gcloud beta compute ssh ${mynode} --project ${myproj} --zone ${myzone}

sudo docker ps | grep your_search
sudo docker exec -it your_pod /bin/bash
```
