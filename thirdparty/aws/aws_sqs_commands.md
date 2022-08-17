## Pull Events from SQS using AWS Cli
```
aws sqs receive-message --queue-url https://sqs.eu-west-2.amazonaws.com/123457890/my-queue-13455.fifo --attribute-names All --message-attribute-name All --max-number-of-messages 1 --profile my_profile_with-role_assume --region eu-west-2
```
