
## Shuffle docker

```
mylan=192.168.30.1
sudo iptables -I INPUT -s ${mylan}/24 -p tcp --dport 3001 -j ACCEPT
sudo iptables -I INPUT -s ${mylan}/24 -p tcp --dport 5001 -j ACCEPT
sudo iptables-save >/etc/iptables/rules.v4
```
