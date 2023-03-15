# API endpoint: https://ji9l7maz08.execute-api.us-east-1.amazonaws.com/default/get_tot_profit_loss

import boto3
import json
from datetime import datetime

# Initialize S3 client
s3 = boto3.client('s3', region_name='us-east-1')

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


def get_total_profit_loss(analysis_result):
    if not analysis_result:
        return {
            'statusCode': 404,
            'body': json.dumps({'error': 'No analysis result found'})
        }

    total_profit_loss = analysis_result['results']['total_profit_loss']
    return {
        'statusCode': 200,
        'body': json.dumps({'total_profit_loss': total_profit_loss})
    }


def lambda_handler(event, context):
    # Fetch the analysis results
    analysis_results = fetch_analysis_results()

    # Get the latest analysis result
    latest_analysis = get_latest_analysis(analysis_results)

    return get_total_profit_loss(latest_analysis)
