## Query data
```
aws --region=eu-west-2 ec2 describe-instances --filters "Name=instance-state-name,Values=running" \
  --query 'Reservations[].Instances[].[Tags[?Key==`environment`] | [].Value]' \
  --output text
```
