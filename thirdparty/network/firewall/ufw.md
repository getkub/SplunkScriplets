## Good Links
- https://ubuntu.com/server/docs/security-firewall


### Scripted format

- One off Enable
```
sudo su -
ufw status
ufw enable
exit
```

```
sudo su -
lan_range="192.168.1.1/24"
dest_port=22
protocol="tcp"

ufw allow proto ${protocol} from ${lan_range} to any port ${dest_port}


```
