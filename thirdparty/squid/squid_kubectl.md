```
kubectl exec "$(kubectl get pod -n mysquidns -l app=sleep -o jsonpath={.items..metadata.name})" -n squid -- sh -c "HTTPS_PROXY=10.10.10.30:3128 curl https://www.google.com"
kubectl exec "$(kubectl get pod -n mysquidns -l app.kubernetes.io/name=my-squid-proxy -o jsonpath={.items..metadata.name})" -n squid -- tail /var/log/squid/access.log
```
