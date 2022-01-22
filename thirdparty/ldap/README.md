## jar file
https://github.com/intoolswetrust/ldap-server


```
# Import user and start server
java -jar ldap-server.jar users.ldif

## to Get information
searchbase="dc=ldap,dc=example"
ldap_server="ldap://127.0.0.1:10389"
bind="uid=admin,ou=system"
bindpw="secret"

ldapsearch -x -b "${searchbase}" -H "${ldap_server}" -D "${bind}" -W
ldapsearch -x -b "${searchbase}" -H "${ldap_server}" -D "${bind}" -w ${bindpw} "objectclass=*"

ldapsearch -x -LLL -H "${ldap_server}" -D "${bind}" -w ${bindpw} -b "${searchbase}" -s sub '(objectClass=*)' 'givenName=username*'

```