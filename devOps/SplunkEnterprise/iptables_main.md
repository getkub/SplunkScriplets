### forwarders 
```
iptables -I INPUT -p udp -m multiport --dports 10514:10520 -j ACCEPT
iptables -I INPUT -p tcp -m multiport --dports 10514:10520 -j ACCEPT
iptables -I INPUT -p tcp --dport 514 -j ACCEPT
```
### VRRP etc
```
iptables -I INPUT -s 10.10.20.0/24 -d 224.0.0.18 -j ACCEPT
iptables-save >/etc/sysconfig/iptables
```
### Generic
```
mylan="192.168.2.0"
iptables -I INPUT -s ${mylan}/24 -p tcp --dport ssh -j ACCEPT
iptables -I INPUT -s ${mylan}/24 -p tcp --dport 8089 -j ACCEPT
iptables -I INPUT -s ${mylan}/24 -p tcp --dport 8000 -j ACCEPT
iptables -I INPUT -s ${mylan}/24 -p tcp --dport 9065 -j ACCEPT
iptables -I INPUT -s ${mylan}/24 -p tcp --dport 9091 -j ACCEPT

iptables-save >/etc/sysconfig/iptables

#ubuntu
iptables-save >/etc/iptables/rules.v4
```

### List open 
```
iptables -L -v -n
```

### Delete (as root)
```
iptables -L -v -n --line-numbers
line_number=xxx
# iptables -D INPUT $line_number
iptables-save >/etc/iptables/rules.v4
```

## Also check
https://github.com/getkub/k8s_kubernetes/tree/main/scripts/iptables

### To reset everything
```
iptables -F
iptables -X
iptables -t nat -F
iptables -t nat -X
iptables -t mangle -F
iptables -t mangle -X
iptables -P INPUT ACCEPT
iptables -P FORWARD ACCEPT
iptables -P OUTPUT ACCEPT
```
