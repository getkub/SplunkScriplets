### indexes vs roles mapping Examples

```
# To show any missing role vs indexes
| rest /services/data/indexes
| stats count by title
| rename title as index
| fields index
| join type=left index [ | rest /services/authorization/roles
    | table title, srchIndexesAllowed
    | mvexpand srchIndexesAllowed
    | rename srchIndexesAllowed as index
    ]


# To find AD/LDAP to roles
| rest /servcies/admin/LDAP-groups splunk_server=local
| table title, roles
```
