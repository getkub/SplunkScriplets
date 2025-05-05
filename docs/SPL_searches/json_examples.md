## Creating JSON object from fields

```
| eval user_object = json_object("user", user_field, "hosts": host)
..
| stats values(user_object) as user_object_valueslist
```
