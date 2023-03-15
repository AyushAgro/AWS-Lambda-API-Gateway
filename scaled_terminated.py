# API endpoint: https://ji9l7maz08.execute-api.us-east-1.amazonaws.com/default/scaled_terminated

import json
import boto3
from botocore.exceptions import ClientError

ec2 = boto3.client('ec2', region_name='us-east-1')


def check_instance_termination(instance_id):
    try:
        response = ec2.describe_instances(InstanceIds=[instance_id])
        instance_state = response['Reservations'][0]['Instances'][0]['State']['Name']

        if instance_state == 'terminated':
            return {
                'terminated': True
            }
        else:
            ec2.terminate_instances(InstanceIds=[instance_id])
            print(f"EC2 instance {instance_id} terminating...")
            waiter = ec2.get_waiter('instance_terminated')
            waiter.wait(InstanceIds=[instance_id])
            print(f"EC2 instance {instance_id} terminated.")
            return {
                'terminated': True
            }
    except ClientError as e:
        print(f"Error checking/terminating EC2 instance: {e}")
        return {
            'statusCode': 500,
            'body': json.dumps({'error': f"Error checking/terminating EC2 instance: {e}"})
        }


def lambda_handler(event, context):
    instance_id = 'i-0e37c562da4746111'  # Replace with your EC2 instance ID
    result = check_instance_termination(instance_id)
    return {
        'statusCode': 200,
        'body': json.dumps(result)
    }
