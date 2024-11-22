## Vault commands

```
az keyvault list --output table
```


## Read from vault

```
vname="myvaultTest"
secretKey="sub-123"

az keyvault secret list --vault-name ${vname} 

az keyvault secret show --vault-name ${vname} --name ${secretKey}

```


## Insert into vault
```
secValue="String1"
secTags='"environment=production" "service=database"'
az keyvault secret set --vault-name ${vname} --name ${secretKey} --value ${secValue}  --tags ${secTags}
az keyvault secret list --vault-name ${vname} --output table

```

#### Put a list as secret
```
az keyvault secret set --vault-name ${vname} --name ${secretKey} \
    --value '[
        "Endpoint=sb://prod-main-eventhub.servicebus.windows.net/;SharedAccessKeyName=RootManageSharedAccessKey;SharedAccessKey=xY7/abcDEF123GHI456JKL789MNO012PQR=;EntityPath=main-tracking-hub",
        "Endpoint=sb://staging-analytics-eventhub.servicebus.windows.net/;SharedAccessKeyName=RootManageSharedAccessKey;SharedAccessKey=pQ9/123XYZ456ABC789DEF012GHI345JKL=;EntityPath=analytics-events-hub",
        "Endpoint=sb://dev-monitoring-eventhub.servicebus.windows.net/;SharedAccessKeyName=RootManageSharedAccessKey;SharedAccessKey=mN5/789KLM012NOP345QRS678TUV901WXY=;EntityPath=system-logs-hub"
    ]'

az keyvault secret list --vault-name ${vname} --output table
```


### delete

```
az keyvault secret delete --vault-name ${vname} --name ${secretKey}
az keyvault secret purge --vault-name ${vname} --name ${secretKey}

```