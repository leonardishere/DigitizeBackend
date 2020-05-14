import json
import boto3
import os
import traceback
import sys
sys.path.append('dependencies') # local location of dependencies
from myawscurl import myawscurl # awscurl modified

CONNECTIONS_TABLE = os.environ['CONNECTIONS_TABLE']
dynamodb_client = boto3.client('dynamodb', region_name='us-west-2')
DEBUG = False

def get_connections():
    connections = dynamodb_client.scan(TableName=CONNECTIONS_TABLE)['Items']
    connections = list(map(lambda conn: conn['connectionId']['S'], connections))
    return connections

def broadcast(message, connections):
    if isinstance(message, dict):
        message = json.dumps(message)
    bad_connections = []
    errors = []
    for connection in connections:
        try:
            kwargs = {
                'request': 'POST',
                'service': 'execute-api',
                'region': 'us-west-2',
                'data': message,
                'uri': 'https://4n16v29io4.execute-api.us-west-2.amazonaws.com/Prod/%40connections/'+connection
            }
            myawscurl(kwargs)
        except Exception as e:
            if DEBUG:
                traceback.print_exc()
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
    message = event['Records'][0]['Sns']['Message']
    connections = get_connections()
    bad_connections, errors = broadcast(message, connections)
    if DEBUG:
        print('bad connections:', bad_connections)
        print('errors:', errors)
    trim_bad_connections(bad_connections)
