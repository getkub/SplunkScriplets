## Various Keytool command
#### Convert from jks12 to pkcs12
```
jks="myjks_file"
storepass="mystorepass"

keytool -importkeystore \
-srckeystore ${jks}.jks -srcstoretype jks -srcstorepass $storepass \
-destkeystore ${jks}.p12 -deststoretype pkcs12 -deststorepass $storepass \

```

```
# Alternatively
keytool -list -rfc -keystore $jks -storepass $storepass | sed "s/^\-*BEGIN [A-Z]-*//g;s/^\-*END [A-Z]-*$//g" > ${jks}.pem

als="ca"
keytool -export -rfc -keystore $jks -storepass $storepass -alias $als -file ${jks}.pem
```


#### PKCS12 to PEM
```
openssl pkcs12 -in ${jks}.p12 -out ${jks}.pem -passin pass:${storepass} -passout pass:${storepass}
```

### PEM can be used in cacert in CURL
