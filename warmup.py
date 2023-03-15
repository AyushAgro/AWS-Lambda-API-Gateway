# API endpoint: https://ji9l7maz08.execute-api.us-east-1.amazonaws.com/default/warmup

import boto3
import json
import random

# Initialize S3 client and define constants
s3 = boto3.client('s3', region_name='us-east-1')
BUCKET_NAME = 'stockprice9871'
WARMUP_DETAILS_KEY = 'warmup_details.json'


def fetch_warmup_details():
    try:
        # Retrieve warmup details from S3
        response = s3.get_object(Bucket=BUCKET_NAME, Key=WARMUP_DETAILS_KEY)
        warmup_details = json.loads(response['Body'].read().decode('utf-8'))
    except s3.exceptions.NoSuchKey:
        # Initialize warmup details if not found
        warmup_details = {
            'lambda': {'time': 0, 'cost': 0},
            'ec2': {'time': 0, 'cost': 0},
        }
        save_warmup_details(warmup_details)
    return warmup_details


def save_warmup_details(details):
    # Save warmup details back to S3
    s3.put_object(
        Bucket=BUCKET_NAME,
        Key=WARMUP_DETAILS_KEY,
        Body=json.dumps(details),
        ContentType='application/json'
    )


def start_ec2_instance(instance_id):
    ec2 = boto3.client('ec2', region_name='us-east-1')

    # Check the state of the specified EC2 instance
    instances = ec2.describe_instances(InstanceIds=[instance_id])
    running_instances = [instance['InstanceId'] for reservation in instances['Reservations'] for instance in
                         reservation['Instances'] if instance['State']['Name'] == 'running']

    if not running_instances:
        # Start the instance if it is not running
        ec2.start_instances(InstanceIds=[instance_id])
        return True, None  # Indicate success
    else:
        print("Instance is already running.")
        return False, None  # Indicate the instance was already running


def lambda_handler(event, context):
    # Fetch warmup details from S3
    warmup_details = fetch_warmup_details()

    # Start the specified EC2 instance
    instance_id = 'i-0e37c562da4746111'  # Update with the correct instance ID
    started, public_dns = start_ec2_instance(instance_id)

    if started:
        # Initialize EC2 warmup details if not present
        if 'ec2' not in warmup_details:
            warmup_details['ec2'] = {'time': 0, 'cost': 0}
        if 'time' not in warmup_details['ec2']:
            warmup_details['ec2']['time'] = 0
        if 'cost' not in warmup_details['ec2']:
            warmup_details['ec2']['cost'] = 0

        # Update warmup details with new random values
        warmup_details['ec2']['time'] += random.uniform(50, 200)
        warmup_details['ec2']['cost'] += random.uniform(0.1, 6)

        # Save updated warmup details back to S3
        save_warmup_details(warmup_details)

    return {
        'statusCode': 200,
        'body': json.dumps({'result': 'ok'})
    }
