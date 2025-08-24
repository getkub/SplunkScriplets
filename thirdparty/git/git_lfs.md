## LFS tips

- Ensure files have LFS enabled

```
# .gitattributes
# Image files
*.jpeg filter=lfs diff=lfs merge=lfs -text
*.jpg filter=lfs diff=lfs merge=lfs -text
*.png filter=lfs diff=lfs merge=lfs -text
*.gif filter=lfs diff=lfs merge=lfs -text
*.svg filter=lfs diff=lfs merge=lfs -text
```

- Profile set for another user
```
# Personal GitHub
Host github.com-personal
  HostName github.com
  User git
  IdentityFile ~/.ssh/id_rsa_personal
  IdentitiesOnly yes

# Work GitHub
Host github.com-work
  HostName github.com
  User git
  IdentityFile ~/.ssh/id_rsa_work
  IdentitiesOnly yes
```

- Set Permissios & Load

```
chmod 600 ~/.ssh/id_rsa_work
chmod 600 ~/.ssh/id_rsa_personal

eval "$(ssh-agent -s)"
ssh-add ~/.ssh/id_rsa_work

git remote set-url origin git@github.com-work:your-work-username/your-repo.git
git remote -v
ssh -T git@github.com-work
```


- LFS migrate command to rewrite history and convert those files to LFS:
```
git lfs migrate import --include="*.png,*.jpg,*.jpeg,*.gif,*.svg"
```