keyDir="/tmp/keys"
mkdir -p $keyDir
account_name="1234567"
vault_url="vault_url_here"

yes y | ssh-keygen -t rsa -N "" -f ${keyDir}/id_rsa
public_key=`cat ${keyDir}/id_rsa.pub`

echo '
{
	"public_key": "'${public_key}'",
	"valid_principals": "ec2-user",
	"ttl": "60m0s"
}
' > ${keyDir}/ssh-ca.json

curl --insecure \
--header "X-Vault-Token": ${client_token} \
--header "X-Vault-Namespace": aws/${account_name} \
--request POST \
--data @${keyDir}/ssh-ca.json \
${vault_url}/v1/ssh/sign/${account_name}-ssh-role | jq -r .data.signed_key > ${keyDir}/id_rsa.signed.pub
