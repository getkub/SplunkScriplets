## Export Variables
```
export AWS_REGION="us-west-1"
export VAULT_SKIP_VERIFY=true
export VAULT_ADDR="https://my_vault_url.com"
export VAULT_NAMESPACE="aws/my-dev-space"
vault login -method=aws role=my-aws-iam-ec2-role
```
