## Ubuntu Setup
- https://www.tecmint.com/install-openldap-server-for-centralized-authentication/

Commands

```
cp /usr/share/slapd/slapd.init.ldif /var/lib/ldap/
ldapadd -Y EXTERNAL -H ldapi:/// -f /etc/ldap/schema/cosine.ldif
ldapadd -Y EXTERNAL -H ldapi:/// -f /etc/ldap/schema/nis.ldif
ldapadd -Y EXTERNAL -H ldapi:/// -f /etc/ldap/schema/inetorgperson.ldif

ldapmodify -Y EXTERNAL -H ldapi:/// -f /tmp/mydomain.ldif
ldapadd -Y EXTERNAL -x -D cn=admin,dc=df,dc=org -W -f /tmp/domainData.ldif
ldapadd -Y EXTERNAL -x -D "cn=admin,dc=df,dc=org" -W  -f /tmp/domainData.ldif

```