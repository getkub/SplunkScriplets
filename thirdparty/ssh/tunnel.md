### SSH Tunnelling

https://github.com/getkub/k8s_kubernetes/blob/main/basic_setup.md#tunnel-from-remote-laptop

```
ssh -L ${localport}:${remoteIP}:${remotePort} ${remoteHostUser}:${remoteHost}
```
