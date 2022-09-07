## IAM policy example
```
{
"Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "",
      "Effect": "Allow",
      "Action": "sts:AssumeRole",
      "Resource": "arn:aws:iam::12345678:role/my-custom-role-automation"
    }
   ]
}

```

## IAM policy Trust example
```
{
  "Version": "2013-10-17",
  "Statement": [
    {
    "Effect": "Allow",
    "Principal": {
    "Federated": "arn:aws:iam::12345678:oidc-provider/oidc.eks.eu-west-1.amazonaws.com/id/E0EB3DCA3B48AAB48AAF9AC4"
    },
  "Action": "sts:AssumeRoleWithWebIdentity",
  "Condition": {
    "StringLike": {
        "oidc.eks.eu-west-1.amazonaws.com/id/E0EB3DCA3B48AAB48AAF9AC4:sub": "system:serviceaccount::ansible"
        }
     }
  }
 ]
}

```
