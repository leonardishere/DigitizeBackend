import json
import boto3
import sys
from time import time

dynamodb_client = boto3.client('dynamodb', region_name='us-west-2')

headers = {
    "Content-Type": "application/json",
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Headers": "Content-Type",
    "Access-Control-Allow-Methods": "OPTIONS,GET,POST,PUT,DELETE"
}

# Lambda handler
def handler(event, context):
    return {
        'statusCode': 200,
        'body': json.dumps(event),
        'headers': headers
    }
