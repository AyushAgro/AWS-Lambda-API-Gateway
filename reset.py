# API endpoint: https://ji9l7maz08.execute-api.us-east-1.amazonaws.com/default/reset

import json
import boto3
from botocore.exceptions import ClientError

# Initialize clients
ec2 = boto3.client('ec2', region_name='us-east-1')
s3 = boto3.client('s3', region_name='us-east-1')

# Constants
INSTANCE_ID = 'i-0e37c562da4746111'  # Replace with your EC2 instance ID


def stop_ec2_instance(instance_id):
    try:
        ec2.stop_instances(InstanceIds=[instance_id])
        print(f"EC2 instance {instance_id} stopping.")
    except ClientError as e:
        print(f"Error stopping EC2 instance: {e}")
        return False
    return True


def lambda_handler(event, context):
    # Stop and terminate the EC2 instance
    instance_stopped = stop_ec2_instance(INSTANCE_ID)

    if not instance_stopped:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': 'Failed to stop EC2 instance'})
        }
    else:
        return {
            'statusCode': 500,
            'body': json.dumps({'result': 'ok'})
        }





