## Compare and show side by side

```
index=admon objectCategory="CN=Person*" (user1 OR user2)
| stats count by name,memberOf
| makemv delim="|" memberOf
| mvexpand memberOf
| rex field=memberOf "CN=(?<ad_group>[^,]+),OU.+"
| fields name,ad_group
| eval user1_group=if(name=="user1", ad_group, null)
| eval user2_group=if(name=="user2", ad_group, null)
| stats values(user1_group) as user1_groups values(user2_group) as 
```

## Compare and Find difference
```
index=admon objectCategory="CN=Person*" (user1 OR user2)
| stats count by name, memberOf
| makemv delim="|" memberOf
| mvexpand memberOf
| rex field=memberOf "CN=(?<ad_group>[^,]+),OU.+"
| fields name, ad_group

| eval user=user1
| eval user_group=ad_group
| fields name user_group
| rename name as user

| append [
    search index=admon objectCategory="CN=Person*" user2
    | stats count by name, memberOf
    | makemv delim="|" memberOf
    | mvexpand memberOf
    | rex field=memberOf "CN=(?<ad_group>[^,]+),OU.+"
    | eval user=user2
    | eval user_group=ad_group
    | fields user user_group
]

| stats values(user) as who by user_group
| where mvcount(who)=1 AND mvindex(who,0)=="user1"
| table user_group
| rename user_group as missing_in_user2
```