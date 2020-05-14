import json

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
        'body': json.dumps({
            'message': 'ping',
            'body': 'pong'
        }),
        'headers': headers
    }
