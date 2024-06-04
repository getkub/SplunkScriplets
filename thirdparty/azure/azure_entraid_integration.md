## EntraID Federation

| Ref    | Details |
| -------- | ------- |
| Application Name | myApplication |
| Application ID | c1723093-1234-48c6-f201cb167e2f |
| Reply URL | https://my-prod.orgname.com/rest/sso/saml/acs |
| User Access URL | https://launcer.myapps.microsoft.com/api/signin/app_id_here?tenantID=728930wb-1234-4c22-abc3-a2328f18b123 |
| App Federation Metadata URL | https://login.microsoftonline.com/tenantID_here/federationmetadata/2007-05/federationmetdata.xml?appid=app_id_here |
| Login URL | https://login.microsoftonline.com/tenantID_here/saml2 |
| Azure AD identifier | https://sts.windows.net/tenantID_here |
| Logout URL | https://login.microsoftonline.com/tenantID_here/saml2 |


### Attributes & Claims
- givenName (user.givenname)
- upn (user.principalname)
- surname (user.surname)
- emailaddress (user.mail)
- name (user.principalname)
- Unique Identifier (user.mail)
