# API endpoint: https://ji9l7maz08.execute-api.us-east-1.amazonaws.com/default/scaled_ready

import boto3
import json

def is_ec2_instance_running(instance_id):
    ec2 = boto3.client('ec2', region_name='us-east-1')

    # Describe instance to check its state
    instances = ec2.describe_instances(InstanceIds=[instance_id])

    # Check if the instance is running
    running_instances = [instance['InstanceId'] for reservation in instances['Reservations'] for instance in reservation['Instances'] if instance['State']['Name'] == 'running']

    return bool(running_instances)

def lambda_handler(event, context):
    # Check if EC2 instance is running
    ec2_instance_id = 'i-0e37c562da4746111'  # Change this to your EC2 instance ID
    ec2_running = is_ec2_instance_running(ec2_instance_id)

    if ec2_running:
        response = {'warm': True}
    else:
        response = {'warm': False}

    return {
        'statusCode': 200,
        'body': json.dumps(response)
    }