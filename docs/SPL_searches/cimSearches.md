### cimSearches Examples

```
| tstas `summariesonly` values(All_Email.recipeient) as R values (All_Email.src_user) as src from datamodel=Email where nodename=All_Email (All_Email.src_user= "*@mycompany.com" or All_Email.src_user= "*@2nd.com") by All_Email.internal_message_id
```
