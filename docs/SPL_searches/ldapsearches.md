### ldapsearches Examples

```
# Physical test
# AD commands
#
ldapsearch -Z -v -x -H ldaps://host21myCompanydc02.myCompany.com:636 -D "myCompany\splunksvc" -w '123;fQ7q' -b "OU=Groups,OU=Europe Region,DC=myCompany,DC=com" "(CN=ABC Splunk*)" | grep 'member|sAMName'
ldapsearch -Z -v -x -H ldaps://host21myCompanydc02.myCompany.com:636 -D "myCompany\splunksvc" -w '123;fQ7q' -b "OU=Users,OU=Europe Region,DC=myCompany,DC=com" "(CN=myname*)"


# Search
|ldapsearch domain=ADMIN search="(&(objectClass=user)(!(objectClass=computer)))"
| search userAccountControl="NORMAL_ACCOUNT"
| eval suffix=""
| eval priority="medium"
| ...

# For groups
|ldapsearch domain=ADMIN search="(&(objectClass=group)(&(cn=SPLNK*)(objectclass=Group)))" basedn="DC=admin,DC=mycmpny,DC=com"


# Combine Groups and User, employeeID etc

|ldapsearch search="(&(objectClass=group)(&(cn=SPLNK*)(objectclass=Group)))" basedn="DC=admin,DC=mycmpny,DC=com" attrs="member"
| mvexpand member
| ldapfilter search="(&(objectClass=user)(distinguishedName=$member$))" attrs="sAMAccountName,displayName"
| table sAMAccountName,displayName

```
