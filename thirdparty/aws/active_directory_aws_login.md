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

- Then Login
```
aws-azure-login --mode=gui # 1st time to allow MFA login
aws-azure-login # for future
```

- Check roles
```
aws sts get-caller-identity
eval $(assume-role my-app-creator)\n
aws sts get-caller-identity
aws s3 ls  # Test
```

Notes
Getting Your Tenant ID and App ID URI
- Your Azure AD system admin should be able to provide you with your Tenant ID and App ID URI. If you can't get it from them, you can scrape it from a login page from the myapps.microsoft.com page.
- Click the chicklet for the login you want.
- In the window the pops open quickly copy the login.microsoftonline.com URL. (If you miss it just try again. You can also open the developer console with nagivation preservation to capture the URL.)
- The GUID right after login.microsoftonline.com/ is the tenant ID.
- Copy the SAMLRequest URL param.
- Paste it into a URL decoder (like this one) and decode.
- Paste the decoded output into the a SAML deflated and encoded XML decoder (like this one).
- In the decoded XML output the value of the Audience tag is the App ID URI.
- You may double-check tenant ID using Attribute tag named tenantid provided in XML.
