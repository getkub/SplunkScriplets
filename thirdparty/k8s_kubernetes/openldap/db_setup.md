
https://docs.bitnami.com/tutorials/create-openldap-server-kubernetes/
```
helm repo add demo https://charts.app-catalog.vmware.com/demo
helm search repo -l demo/mariadb-galera
```

** Amend values :  values.yaml **


```
helm install -f values.yaml my-release demo/mariadb-galera
kubectl get sts -l app.kubernetes.io/instance=my-release -w
kubectl get service

```

### Test connections
```
echo "$(kubectl get secret openldap -n default -o json | jq -r .data.users | base64 --decode)"
echo "$(kubectl get secret openldap -n default -o json | jq -r .data.passwords | base64 --decode)"

kubectl run mariadb-galera-client --rm --tty -i --restart='Never' --namespace default --image gcr.io/sys-2b0109it/demo/bitnami/mariadb-galera:10.4.13-centos-7-r20 --command -- bash
# mysql -h my-release-mariadb-galera -u user01 -ppassword01 my_database
kubectl logs OPENLDAP-POD-NAME

```
