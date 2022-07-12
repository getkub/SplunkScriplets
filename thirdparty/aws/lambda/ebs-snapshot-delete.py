import boto3
import datetime
from datetime import timezone, timedelta, datetime

def lambda_handler(event, context):

    client = boto3.client('ec2', region_name = 'eu-west-2')
    snapshots = client.describe_snapshots(OwnerIds=['self'])
    print ("Deleting snapshots older than 10 days")
    print (snapshots)
    
    for snapshot in snapshots['Snapshots']:
        start_time = snapshot['StartTime']
        id = snapshot['SnapshotId']
        delete_time = datetime.now(timezone.utc) - timedelta(days=10)
        if delete_time > start_time:
            print(f"Start time {start_time} Delete time {delete_time}")
            client.delete_snapshot(SnapshotId = id)
            print(f"Snapshot with id {id} is deleted!" )
 
