- Install Assume-role
```
brew install remind101/formulae/assume-role
```

- append the profiles content 
```
cat append_contents_to_existing_aws_config_file >>  ~/.aws/config file.
```

- Setup environment
```
cp set-aws-env.sh   /usr/local/bin/set-aws-env

chmod 755 /usr/local/bin/set-aws-env

```

- Add alias alias set-aws-env="source set-aws-env" in ~/.zshrc file

```
cp ~/.zshrc  ~/zshrc-backup
echo ‘alias set-aws-env="source set-aws-env"’ >> ~/.zshrc

set-aws-env
```
