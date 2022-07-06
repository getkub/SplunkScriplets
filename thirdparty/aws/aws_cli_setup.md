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
cp setup_aws_env.sh   /usr/local/bin/setup_aws_env

chmod 755 /usr/local/bin/setup_aws_env

```

- Add alias alias

```
cp ~/.zshrc  ~/zshrc-backup
echo ‘alias setup_aws_env="source setup_aws_env"’ >> ~/.zshrc

setup_aws_env
```
