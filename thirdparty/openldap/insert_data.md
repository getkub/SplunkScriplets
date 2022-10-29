### Insert data to ldap
```
password="adminpassword"
ldapserver="127.0.0.1:1389"
ldifFile="/tmp/newusers.ldif"
ldapadd -x -D "cn=admin,dc=df,dc=org" -w $password -H ldap://${ldapserver} -f ${ldifFile}
ldapmodify -a -x -D "cn=admin,dc=df,dc=org" -w $password -H ldap://${ldapserver} -f ${ldifFile}
```
