
```
external_ip=192.168.2.81
host_domain=192-168-2-82.nip.io

helm upgrade --install gitlab gitlab/gitlab \
  --timeout 600s \
  --set global.hosts.domain=${host_domain) \
  --set global.hosts.externalIP=${external_ip} \
  --set certmanager-issuer.email=kinbsk@gmail.com \
  --namespace gitlab
  ```
