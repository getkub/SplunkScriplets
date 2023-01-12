## Token extraction method
```
aws_account_name=1123453235
myorg="myapp-eu-west-1.$aws_account_name.aws.myorg.com"
token=$(vault login -method=aws role="$aws_account_name"-aws-iam-auth-ec2-role -format=json | jq -r .auth.client_token)
vault write -format=json pki/issue/${myorg}.role common_name="myapp-eu-west-1.${myorg}"  > /tmp/vault.crt

cat /tmp/vault.crt | jq -r .data.certificate > /tmp/my-cer.crt
cat /tmp/vault.crt | jq -r .data.private_key > /tmp/my-key.pem
cat /tmp/vault.crt | jq -r .data.ca_chain[0] > /tmp/my-ca-chain.crt
```

## Token extraction method - via API
```
MY_KEY_DIR="org/department"
# Extract the key from the DIR

curl \
-H "X-Vault-Token: $CLIENT_TOKEN" \
-H "X-Vault-Namespace: $NS" \
-X GET ${VAULT_URL}/v1/secrets/data/${MY_KEY_DIR}

```


## Token Update method
```
aws secretsmanager put-secret-value --secret-id myapp-eu-west-1.${myorg} --region eu-west-1 --secret-string file:///tmp/my-key.pem
```
