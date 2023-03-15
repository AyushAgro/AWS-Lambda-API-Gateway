# API endpoint: https://ji9l7maz08.execute-api.us-east-1.amazonaws.com/default/get_endpoints

import boto3
import json

# Initialize the API Gateway client
apigateway = boto3.client('apigateway', region_name='us-east-1')


def list_api_endpoints(rest_api_id):
    # Retrieve the resources (endpoints) for the specified REST API
    response = apigateway.get_resources(restApiId=rest_api_id)
    resources = response.get('items', [])

    endpoints = []
    for resource in resources:
        resource_id = resource.get('id')
        path = resource.get('path')
        methods = resource.get('resourceMethods', {}).keys()

        for method in methods:
            callstring = f'curl -X {method} "https://{rest_api_id}.execute-api.us-east-1.amazonaws.com/default{path}"'
            endpoints.append({'endpoint': callstring})

    return endpoints


def lambda_handler(event, context):
    rest_api_id = 'ji9l7maz08'  # Replace with your REST API ID

    try:
        endpoints = list_api_endpoints(rest_api_id)
        return {
            'statusCode': 200,
            'body': json.dumps(endpoints)
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }
