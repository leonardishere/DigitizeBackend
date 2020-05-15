import json
import boto3
import os
import sys
sys.path.append('dependencies') # local location of dependencies
from student import Student
from activecheckin import ActiveCheckin

ACTIVE_CHECKINS_TABLE = os.environ['ACTIVE_CHECKINS_TABLE']
dynamodb_client = boto3.client('dynamodb', region_name='us-west-2')

headers = {
    "Content-Type": "application/json",
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Headers": "Content-Type",
    "Access-Control-Allow-Methods": "OPTIONS,GET,POST,PUT,DELETE"
}

def get_active_checkins():
    arr = dynamodb_client.scan(TableName=ACTIVE_CHECKINS_TABLE)['Items']
    arr = [ActiveCheckin(checkin) for checkin in arr]
    arr.sort(key=lambda checkin: checkin.CardReaderID)
    data = [checkin.to_dict() for checkin in arr]
    return {
        'statusCode': 200,
        'body': json.dumps([{
            'msg': 'Received active checkins data',
            'msgType': 'ignore',
            'data': {
                'active_checkins': data
            }
        }]),
        'headers': headers
    }

# Lambda handler
def handler(event, context):
    try:
        return get_active_checkins()
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'Error': str(e)}),
            'headers': headers
        }
