# API endpoint: https://ji9l7maz08.execute-api.us-east-1.amazonaws.com/default/terminate

import json
import boto3
from botocore.exceptions import ClientError

ec2 = boto3.client('ec2', region_name='us-east-1')

def terminate_ec2_instance(instance_id):
    try:
        response = ec2.terminate_instances(InstanceIds=[instance_id])
        print(f"EC2 instance {instance_id} terminating.")
        return response
    except ClientError as e:
        print(f"Error terminating EC2 instance: {e}")
        return {
            'statusCode': 500,
            'body': json.dumps({'error': f"Error terminating EC2 instance: {e}"})
        }

def lambda_handler(event, context):
    instance_id = 'i-0e37c562da4746111'  # Replace with your EC2 instance ID
    response = terminate_ec2_instance(instance_id)
    return {
        'statusCode': 200,
        'body': json.dumps({'result': 'ok'})
    }
