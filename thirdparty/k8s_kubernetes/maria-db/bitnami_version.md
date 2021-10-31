## Install
```
helm repo add bitnami https://charts.bitnami.com/bitnami
helm install my-release bitnami/mariadb-galera
```


## Uninstall
```
kubectl scale sts my-release-mariadb-galera --replicas=0
helm uninstall  my-release
```
