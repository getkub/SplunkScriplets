## To login from single sign-on (eg Azure AD)
- Assuming `AWS cli is installed, python3, pip, brew, nodejs` is installed
- INstall other dependencie
```
pip3 install boto3
# Install AWS Azure login utility
npm install -g aws-azure-login
```

- Configure AWS/Azure login
```
aws-azure-login --configure
```

- Sample below
```
azure_tenant_id=xxxxxx-e470-1234-e402-yyyyyyyyy
azure_app_id_uri=https://signin.aws.amazon.com/saml
azure_default_username=login_email_or_org_id
azure_default_remember_me=true
azure_default_role_arn=
azure_default_duration_hours=6
region=eu-west-1
```
