## Tainting a node
```
kubectl taint nodes my_node node.kubernetes.io=unschedulable:NoSchedule
kubectl taint nodes mynode dedicated=experimental:NoSchedule
```


## To Remove taint
```
kubectl taint nodes my_node node.kubernetes.io=unschedulable:NoSchedule-
```
