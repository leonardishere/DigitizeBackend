import json
import boto3
import sys
sys.path.append('dependencies') # local location of dependencies
from myawscurl import myawscurl # awscurl modified

dynamodb_client = boto3.client('dynamodb', region_name='us-west-2')
sts = boto3.client('sts', region_name='us-west-2')

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
    connections = list(map(lambda conn: conn['connectionId']['S'], connections))
    print('connections:', connections)
    return connections

def broadcast(message, connections):
    bad_connections = []
    errors = []
    for connection in connections:
        try:
            kwargs = {
                'request': 'POST',
                'service': 'execute-api',
                'region': 'us-west-2',
                'data': message,
                'uri': 'https://soagcpz8cl.execute-api.us-west-2.amazonaws.com/Prod/%40connections/'+connection
            }
            myawscurl(kwargs, sts=sts)
        except Exception as e:
            bad_connections.append(connection)
            errors.append(str(e))
    return bad_connections, errors

def trim_bad_connections(connections):
    for connection in connections:
        dynamodb_client.delete_item(
            TableName='DigitizeConnections',
            Key={'connectionId':{'S':connection}}
        )

# Lambda handler
def handler(event, context):
    try:
        message = event['body'] if 'body' in event else event
        connections = get_connections()
        bad_connections, errors = broadcast(message, connections)
        #trim_bad_connections(bad_connections)
        return {
            'statusCode': 200,
            'body': json.dumps({
                'connections': connections,
                'bad_connections': bad_connections,
                'errors': errors
            }),
            'headers': headers
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({
                'Error': str(e)
            }),
            'headers': headers
        }
