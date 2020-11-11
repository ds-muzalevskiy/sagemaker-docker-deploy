import os
import io
import boto3
import json
import csv

ENDPOINT_NAME = os.environ['ENDPOINT_NAME']
runtime= boto3.client('runtime.sagemaker')

def lambda_handler(event, context):
    print("Received event: " + json.dumps(event, indent=2))
    
    data = json.loads(json.dumps(event))
    payload = data['data']
    print(payload)
    
    response = runtime.invoke_endpoint(EndpointName=ENDPOINT_NAME,
                                       ContentType='text/csv',Body=payload)
    result = json.loads(response['Body'].read().decode())
    
    if(result=="0"):
        result="Not Failure"
    else:
        result="Failure"
    return result