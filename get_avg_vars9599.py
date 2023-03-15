# API endpoint: https://ji9l7maz08.execute-api.us-east-1.amazonaws.com/default/get_avg_vars9599

import boto3
import json
from datetime import datetime

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


# Function to get the latest analysis result based on timestamp
def get_latest_analysis(analysis_results):
    if not analysis_results:
        return None

    # Sort the keys by timestamp
    sorted_timestamps = sorted(analysis_results.keys(), key=lambda x: datetime.fromisoformat(x))
    latest_timestamp = sorted_timestamps[-1]
    return analysis_results[latest_timestamp]


# Function to calculate the average of var95 and var99
def get_avg_vars9599(analysis_result):
    if not analysis_result:
        return {
            'statusCode': 404,
            'body': json.dumps({'error': 'No analysis result found'})
        }

    var95 = analysis_result['results']['var95']
    var99 = analysis_result['results']['var99']
    avg_var95 = sum(var95) / len(var95) if var95 else 0
    avg_var99 = sum(var99) / len(var99) if var99 else 0
    return {
        'statusCode': 200,
        'body': json.dumps({'var95': avg_var95, 'var99': avg_var99})
    }


def lambda_handler(event, context):
    # Fetch the analysis results
    analysis_results = fetch_analysis_results()

    # Get the latest analysis result
    latest_analysis = get_latest_analysis(analysis_results)

    # Calculate and return the average of var95 and var99
    return get_avg_vars9599(latest_analysis)