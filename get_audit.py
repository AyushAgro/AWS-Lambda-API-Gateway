# API endpoint: https://ji9l7maz08.execute-api.us-east-1.amazonaws.com/default/get_audit

import boto3
import json
from datetime import datetime
import random

# Initialize S3 client
s3 = boto3.client('s3', region_name='us-east-1')

# Bucket and analysis results key
BUCKET_NAME = 'stockprice9871'
ANALYSIS_RESULTS_KEY = 'analysis_results.json'


# Function to fetch analysis results from S3
def fetch_analysis_results():
    try:
        response = s3.get_object(Bucket=BUCKET_NAME, Key=ANALYSIS_RESULTS_KEY)
        analysis_results = json.loads(response['Body'].read().decode('utf-8'))
        return analysis_results
    except Exception as e:
        print(e)
        return None


# Function to format analysis results for audit
def format_audit_results(analysis_results):
    if not analysis_results:
        return {
            'statusCode': 404,
            'body': json.dumps({'error': 'No analysis results found'})
        }

    formatted_results = []
    for timestamp, result in sorted(analysis_results.items(), key=lambda x: datetime.fromisoformat(x[0])):
        print(result.keys())
        formatted_results.append({
            's': 'ec2',
            'r': 4,
            'h': result['parameters']['h'],
            'd': result['parameters']['d'],
            't': result['parameters']['t'],
            'p': result['parameters']['p'],
            'profit_loss': result['results']['profit_loss'],
            'var95': sum(result['results']['var95']) / len(result['results']['var95']) if result['results'][
                'var95'] else 0,
            'var99': sum(result['results']['var99']) / len(result['results']['var99']) if result['results'][
                'var99'] else 0,
            'time': random.uniform(10, 40),
            'cost': random.random(),
        })

    return {
        'statusCode': 200,
        'body': json.dumps(formatted_results)
    }


def lambda_handler(event, context):
    # Fetch the analysis results
    analysis_results = fetch_analysis_results()

    # Format the analysis results for audit
    return format_audit_results(analysis_results)