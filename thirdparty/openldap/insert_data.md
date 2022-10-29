### Insert data to ldap
```

ldapadd -x -D "cn=admin,dc=df,dc=org" -w password -H ldap:// -f newusers.ldif
ldapmodify -a -x -D "cn=admin,dc=df,dc=org" -w password -H ldap:// -f newgroups.ldif
```
