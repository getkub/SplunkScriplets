## Requires proxy, email, user.name, pull strategy
```
proxy=mysite.company.com:8080
myemail=myemail@example.com
myuserid=my_user

git config --global http.proxy http://${proxy}
git config --global user.email $myemail
git config --global user.name $myuserid
git config --global pull.rebase false

# git config --global http.sslverify false
# git config --edit --global

# Add certificate as follows
git_uri="git.myhost.com:443"
cert_file="/home/repo_base/git_cert.pem"
openssl s_client -connect ${git_uri} 2>/dev/null </dev/null | sed -ne '/-BEGIN CERTIFICATE-/,/-END CERTIFICATE-/p' > $cert_file
git config --global --unset http.sslverify
git config --global http.sslCAInfo $cert_file

## If above doesn't work in some cases , try OVERRIDING using variables
# export GIT_SSL_CAINFO="C:\mylocation\git_cert.pem"
```

### Using tokens 
- Navigate to project tokens (settings/access_tokens)
- Create token with relevant scope 
- Ensure you take the token out (as it will not appear again)
```
# $myuserid
token=26N22352cLVPSpcG-e_7
proj=myproj
repo=myrepo
domain=gitlab.xyz.nip.io
url="https://${myuserid}:${token}@${domain}/${proj}/${repo}.git"

git clone $url
cd $repo
```
