## DIG command with xargs to curl
```
dig +short host.docker.internal | xargs -I{} curl -s http://{}:8200/v1/sys/seal-status
```
