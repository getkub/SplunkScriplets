# To find keys in a pem key . Also good to check/verify the passphrase supplied
```
openssl rsa -in /opt/splunk/etc/auth/server.pem -text
```
# TO Check connectivity similar to Curl
```
openssl s_client -connect  <remoteServer>:<port>
openssl x509 req -config <my_config_key> in <server.key> -out <my_cert.crt> - days 3650
```

# Generate NEW CERT directly from config file (for self-signed)
```
openssl req -x509  -new -config <my_config_key> in <server.key> -out <my_cert.crt> - days 3650
```

# For existing
```
openssl req -x509  -new -config <my_config_key> -key <server.key> -out <my_cert.crt> - days 3650
```

## To check if Key matches with cert and both md5sum should match
```
keyfile="/tmp/file/file.key"
cert="/tmp/file/mycert.crt"
openssl rsa -modulus -noout -in $keyfile | openssl md5
openssl x509 -modulus -noout -in $cert | openssl md5
```

# Convert to pkcs8
```
keyfile="/tmp/file/file.key"
password_of_pk8="mypass"
pkcs8file="/tmp/file/file.pk8"
openssl pkcs8 -in $keyfile -topk8 -passout pass:${password_of_pk8} -out  $pkcs8file
```

## Checking
```
#  Checking whether the hostname on the certificate matches the name you want
openssl s_client -verify_hostname example.com  -connect serverfault.com:443

# Checking whether the certificate is from a trusted CA
openssl s_client -verify 2 -connect serverfault.com:443
```
