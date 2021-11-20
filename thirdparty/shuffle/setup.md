
## Shuffle docker
```
git clone https://github.com/frikky/Shuffle
cd Shuffle
mkdir shuffle-database
sudo chown 1000:1000 -R shuffle-database
docker-compose up -d
```


## Local firewall enable
```
sudo su - 
mylan=192.168.30.1
iptables -I INPUT -s ${mylan}/24 -p tcp --dport 3001 -j ACCEPT
iptables -I INPUT -s ${mylan}/24 -p tcp --dport 3443 -j ACCEPT
iptables -I INPUT -s ${mylan}/24 -p tcp --dport 5001 -j ACCEPT
iptables-save >/etc/iptables/rules.v4
```
