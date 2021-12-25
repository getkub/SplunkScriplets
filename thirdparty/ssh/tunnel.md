### SSH Tunnelling

https://github.com/getkub/k8s_kubernetes/blob/main/basic_setup.md#tunnel-from-remote-laptop

```
ssh -L ${localport}:${remoteIP}:${remotePort} ${remoteHostUser}:${remoteHost}
```

## SSH & TLS
HTTPS connection can be redirected via SSH port forwarding - however the SSL/TLS certificate validation will fail in such cases as the host name does not match
https://superuser.com/questions/347415/is-it-possible-to-tunnel-https-traffic-via-ssh-tunnel-with-standard-ssh-programs
