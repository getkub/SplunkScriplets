### Insert data to ldap
```
password="adminpassword"
ldapserver="127.0.0.1:1389"
ldifFile="/tmp/newusers.ldif"
mydn="dc=example,dc=org"
ldapadd -x -D $mydn -w $password -H ldap://${ldapserver} -f ${ldifFile}
ldapmodify -a -x -D $mydn -w $password -H ldap://${ldapserver} -f ${ldifFile}

ldapsearch -H ldap://${ldapserver} -x -s base -b "" -LLL "+"
#ldapadd -x -W -D "cn=ldapadm,${mydn}" -f /etc/openldap/slapd.d/xxxxx.ldif

```


## Password changes
- https://www.digitalocean.com/community/tutorials/how-to-change-account-passwords-on-an-openldap-server

```
ldappasswd -H ldap://${ldapserver} -x -D $mydn -W -A -S
ldappasswd -H ldap://${ldapserver} -x -D $mydn -w old_passwd -a old_passwd -S
```
