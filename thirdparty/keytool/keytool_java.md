
```
chain_name="my-chain-1"
keypass="changeit"
```

## Linux OS
```
Linux normally has in  /etc/pki/ca-trust/source/anchors/*.pem
```


### Java
```
keytool -import -trustcacerts -keystore $JAVA_HOME/lib/security/cacerts -storepass $keypass -noprompt -alias $chain_name -file $chain_name

keytool -delete -alias $chain_name -keystore $JAVA_HOME/lib/security/cacerts -storepass $keypass
```
