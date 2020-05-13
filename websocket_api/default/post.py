import json
import boto3
import os
import sys
sys.path.append('dependencies') # local location of dependencies

BROADCAST_TOPIC = os.environ['BROADCAST_TOPIC']
sns_client = boto3.client('sns', region_name='us-west-2')

headers = {
    "Content-Type": "application/json",
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Headers": "Content-Type",
    "Access-Control-Allow-Methods": "OPTIONS,GET,POST,PUT,DELETE"
}

# Lambda handler
def handler(event, context):
    # broadcast
    try:
        broadcast_msg = json.dumps([{
            'msgType': 'info',
            'msg': 'Websocket default route received message: ' + json.dumps(event)
        }])
        sns_response = sns_client.publish(
            TopicArn=BROADCAST_TOPIC,
            Message=broadcast_msg
        )
    except Exception as e:
        return {
            'statusCode': 500,
            'body': "Error: Could not broadcast. " + str(e),
            'headers': headers
        }

    # success
    http_response = {
        'statusCode': 200,
        'body': json.dumps({
            'msgType': 'info',
            'msg': 'broadcasted'
        }),
        'headers': headers
    }
    return http_response
    #return post_student(event['body'])
