import json
import boto3
#import awscurl
import subprocess

#subprocess.run(["pip3", "install", "awscurl", "--user"])

dynamodb_client = boto3.client('dynamodb', region_name='us-west-2')

headers = {
    "Content-Type": "application/json",
    "Access-Control-Allow-Origin": "*", #"https://digitize.aleonard.dev",
    "Access-Control-Allow-Headers": "Content-Type",
    "Access-Control-Allow-Methods": "OPTIONS,POST,GET"
}

def get_connections():
    connections = dynamodb_client.scan(
        TableName='DigitizeConnections'
    )['Items']
    print('connections:', connections)
    return connections

def broadcast(message, connections):
    for connection in connections:
        subprocess.run([
            "awscurl",
            "--region", "us-west-2",
            "-X", "POST",
            "-d", message,
            "https://soagcpz8cl.execute-api.us-west-2.amazonaws.com/Prod/%40connections/"+connection['connectionId']['S']
        ])

# Lambda handler
def handler(event, context):
    try:
        message = event['body']
        connections = get_connections()
        broadcast(message, connections)
        return {
            'statusCode': 200,
            'headers': headers
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'Error': str(e)})
            'headers': headers
        }
