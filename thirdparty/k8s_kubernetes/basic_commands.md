

### K8s commands
```
namepsace="default"
podname=""
kubectl get deployment -n ${namepsace}
kubectl get pods -n ${namepsace}
kubectl get pods --all-namespaces
kubectl get pod ${podname} -n ${namepsace} -o yaml
```

### Scale within deployment
```
kubectl get deployment -n ${namepsace}
kubectl scale --current-replicas=2 --replicas=3 deployment/nginx-deployment -n ${namepsace}
kubectl scale --replicas=4 deployment/nginx-deployment -n ${namepsace}
```

### Running in a loop
```
for mypv in $(kubectl get pv -o jsonpath="{.items[*].metadata.name}" | grep -v Terminating);
do
  # kubectl patch pv $mypv -p '{"metadata":{"finalizers":null}}'
  kubectl get pods
done
```
