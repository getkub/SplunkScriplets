## Token extraction method
```
token=$(vault login -method=aws role="$aws_account_name"-aws-iam-auth-ec2-role -format=json | jq -r .auth.client_token)
vault write -format=json pki/issue/"$aws_account_name".aws.myorg.com.role common_name="myapp-eu-west-1.$aws_account_name.aws.myorg.com"  > /tmp/vault.crt

cat /tmp/vault.crt | jq -r .data.certificate
cat /tmp/vault.crt | jq -r .data.ca_chain[0]
```
