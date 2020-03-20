import json

# Lambda handler
def handler(event, context):
    return {
        'statusCode': 200,
        'headers': {
            "Access-Control-Allow-Origin": "https://digitize.aleonard.dev",
            "Access-Control-Allow-Headers": "Content-Type",
            "Access-Control-Allow-Methods": "OPTIONS,POST,GET"
        },
        'body': json.dumps(response)
    }
