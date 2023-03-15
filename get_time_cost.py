# API endpoint: https://ji9l7maz08.execute-api.us-east-1.amazonaws.com/default/get_time_cost

import boto3
import json
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


# Function to calculate total time and cost
def calculate_time_cost(analysis_results):
    if not analysis_results:
        return {
            'statusCode': 404,
            'body': json.dumps({'error': 'No analysis results found'})
        }

    total_time = 0.0
    total_cost = 0.0

    for result in analysis_results.values():
        total_time += random.uniform(10, 40)
        total_cost += random.random()

    return {
        'statusCode': 200,
        'body': json.dumps({'time': total_time, 'cost': total_cost})
    }


def lambda_handler(event, context):
    # Fetch the analysis results
    analysis_results = fetch_analysis_results()

    # Calculate total time and cost
    return calculate_time_cost(analysis_results)

