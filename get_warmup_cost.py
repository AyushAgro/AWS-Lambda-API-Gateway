# API endpoint: https://ji9l7maz08.execute-api.us-east-1.amazonaws.com/default/get_warmup_cost

import boto3
import json

# Initialize AWS services
s3 = boto3.client('s3', region_name='us-east-1')

# Bucket name and keys
BUCKET_NAME = 'stockprice9871'
WARMUP_DETAILS_KEY = 'warmup_details.json'


def fetch_warmup_details():
    try:
        response = s3.get_object(Bucket=BUCKET_NAME, Key=WARMUP_DETAILS_KEY)
        warmup_details = json.loads(response['Body'].read().decode('utf-8'))
    except s3.exceptions.NoSuchKey:
        warmup_details = {
            'lambda': {'time': 0, 'cost': 0},
            'ec2': {'time': 0, 'cost': 0},
            'emr': {'time': 0, 'cost': 0},
            'ecs': {'time': 0, 'cost': 0}
        }
        save_warmup_details(warmup_details)

    return warmup_details


def lambda_handler(event, context):
    warmup_details = fetch_warmup_details()
    return warmup_details

