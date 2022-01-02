######################
# Become a Certificate Authority
######################
# https://stackoverflow.com/questions/7580508/getting-chrome-to-accept-self-signed-localhost-certificate
certDir="/tmp/gen_cert"
mkdir -p ${certDir}
caConf=${certDir}/ca.conf
certConf=${certDir}/cert.conf

if [ ! -f "$caConf" ] || [ ! -f "$certConf" ]; then
    echo "Config File: $caConf OR $certConf NOT found.. Exiting"
    exit 10
fi

# echo " *** Generate private key *** "
# openssl genrsa -des3 -out ${certDir}/myCA.key 2048
# echo " *** Generate root certificate *** "
# openssl req -x509 -new -nodes -key ${certDir}/myCA.key -sha256 -days 825 -out ${certDir}/myCA.pem

echo " *** Generate CA key & CA pem *** "
openssl req -x509 -newkey rsa:4096 -keyout ${certDir}/myCA.key -out ${certDir}/myCA.pem -config $caConf -days 3650 -nodes


######################
# Create CA-signed certs
######################

NAME=mydev.test # Use your own domain name
echo " *** Generate a private key *** "
openssl genrsa -out ${certDir}/$NAME.key 2048
echo " *** Create a certificate-signing request *** "
openssl req -new -key ${certDir}/$NAME.key -out ${certDir}/$NAME.csr -config $certConf -nodes
echo " *** Create the signed certificate *** "
openssl x509 -req -in ${certDir}/$NAME.csr -CA ${certDir}/myCA.pem -CAkey ${certDir}/myCA.key -CAcreateserial \
-out ${certDir}/$NAME.crt -days 365 -sha256 -extensions 'my_server_exts'

echo "Certificates are now ready at ${certDir}/ "