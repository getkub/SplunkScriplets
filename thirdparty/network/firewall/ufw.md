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

- Enable a port access
```
sudo su -
lan_range="192.168.1.0/24"
dest_port=22
protocol="tcp"

ufw allow proto ${protocol} from ${lan_range} to any port ${dest_port}
ufw status

```

- Dry run & other tips
```
sudo su -
ufw --dry-run allow http

ufw status verbose
ufw status numbered
```

- Apps Example
```
sudo su -
ufw app list
lan_range="192.168.1.0/24"
ufw allow from ${lan_range} to any app Samba
ufw app info Samba
```

