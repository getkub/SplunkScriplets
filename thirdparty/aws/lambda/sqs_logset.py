import gzip
import json
import base64
import boto3
import time

def lambda_handler(event, context):
    sqs = boto3.client('sqs')
    account = boto3.client('sts').get_caller_identity()['Account']

    queue_url = "https://sqs.eu-west-1.amazonaws.com/12345567928/my-app-{}.fifo".format(account)
    cw_data = event['awslogs']['data']
    compressed_payload = base64.b64decode(cw_data)
    uncompressed_payload = gzip.decompress(compressed_payload)
    payload = json.loads(uncompressed_payload)
    log_events = payload['logEvents']
    log_group = payload['logGroup']
    log_stream = payload['logStream']
    event=    {}
    for log_event in log_events:
        event['AccountID']=account
        event['LogGroup']=log_group
        event['LogStream']=log_stream
        event['Log']=log_event
        response = sqs.send_message(
            QueueUrl=queue_url,
            MessageGroupId="my_logging",
            MessageDeduplicationId="%.20f" % time.time(),
            MessageBody=json.dumps(event)
        )
