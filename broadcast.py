dynamodb_client = None
headers = None

def get_connections():
    connections = dynamodb_client.scan(
        TableName='DigitizeConnections'
    )['Items']
    connections = list(map(lambda conn: conn['connectionId']['S'], connections))
    print('connections:', connections)
    return connections

def broadcast(message, connections):
    for connection in connections:
        #gwmapi.post_to_connection(Data=message,ConnectionId=connection)
        kwargs = {
            'request': 'POST',
            'service': 'execute-api',
            'region': 'us-west-2',
            'data': message,
            'uri': 'https://soagcpz8cl.execute-api.us-west-2.amazonaws.com/Prod/%40connections/'+connection
        }
        myawscurl(kwargs)

# Lambda handler
def handler(event, context):
    try:

        import json
        import boto3
        import sys
        sys.path.append('dependencies') # local location of dependencies
        #import awscurl # modified
        from myawscurl import myawscurl

        dynamodb_client = boto3.client('dynamodb', region_name='us-west-2')
        #gwmapi = boto3.client('apigatewaymanagementapi', region_name='us-west-2')

        headers = {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*", #"https://digitize.aleonard.dev",
            "Access-Control-Allow-Headers": "Content-Type",
            "Access-Control-Allow-Methods": "OPTIONS,POST,GET"
        }

        message = event['body']
        print('message:', message)
        connections = get_connections()
        broadcast(message, connections)
        return {
            'statusCode': 200,
            'body': json.dumps({
                'message': 'sent message to ' + str(connections)
            }),
            'headers': headers
        }
    except Exception as e:
        traceback.print_exc()
        return {
            'statusCode': 500,
            'body': json.dumps({'Error': str(e)}),
            'headers': headers
        }
