###  AWS sts assume role in one command
- https://stackoverflow.com/questions/63241009/aws-sts-assume-role-in-one-command
- 
```
export $(printf "AWS_ACCESS_KEY_ID=%s AWS_SECRET_ACCESS_KEY=%s AWS_SESSION_TOKEN=%s" \
$(aws sts assume-role \
--role-arn arn:aws:iam::123456789012:role/MyAssumedRole \
--role-session-name MySessionName \
--query "Credentials.[AccessKeyId,SecretAccessKey,SessionToken]" \
--output text))
```
