## Getting or sharing data outside of o365
```
index=firewall_index object_type=File shared_domains="*" shared_domains!=""
| stats latest(owner) as Owner latest(user) as User latest(exposure) as Exposure latest(shared_with) as Shared_With latest(shared_domains) as Shared_Domains by object_id
| eval ListItemUniqueId = object_id, Shared_With=split(Shared_With, ","), Shared_Domains=split(Shared_Domains, ",")
| lookup allowed_domains.csv domain AS Shared_Domains OUTPUT allowed
| where isnull(allowed) OR allowed="no"
| table ListItemUniqueId Owner User Exposure Shared_Domains Shared_With

| append [
  search index=o365_index object_category=file user!="app@sharepoint"
  | eval New_FileClassification=case(
      match(SensitivityLabelId,"<internal_id_1>"),"Internal",
      match(SensitivityLabelId,"<internal_id_2>"),"Confidential",
      match(SensitivityLabelId,"<internal_id_3>"),"Public",
      match(SensitivityLabelId,"<internal_id_4>"),"Highly Confidential",
      true(),"NA"
    )
  | stats latest(ListItemUniqueId) as ListItemUniqueId latest(New_FileClassification) as New_FileClassification by ObjectId
  | lookup sensitive_file.csv File AS ObjectId OUTPUT FileClassification as Old_FileClassification
  | eval Old_FileClassification=coalesce(Old_FileClassification, New_FileClassification)
]

| stats values(*) as * by ListItemUniqueId
| where isnotnull(Shared_Domains) AND isnotnull(ObjectId)
| eval severity=if(
    match(Old_FileClassification,"Confidential")
    AND NOT match(New_FileClassification,"NA")
    AND New_FileClassification != Old_FileClassification,
    "critical",
    "medium"
  )

```
