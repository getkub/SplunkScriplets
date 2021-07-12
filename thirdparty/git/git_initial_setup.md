## Requires proxy, email, user.name, pull strategy
```
proxy=mysite.company.com:8080
myemail=myemail@example.com
myuserid=my_user

git config --global http.proxy http://${proxy}
git config --global user.email $myemail
git config --global user.name $myuserid
git config --global pull.rebase false

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
