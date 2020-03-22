import json
import boto3
import sys
from time import time

sys.path.append('dependencies') # local location of dependencies
from student import Student
from activecheckin import ActiveCheckin

dynamodb_client = boto3.client('dynamodb', region_name='us-west-2')

headers = {
    "Content-Type": "application/json",
    "Access-Control-Allow-Origin": "*", #"https://digitize.aleonard.dev",
    "Access-Control-Allow-Headers": "Content-Type",
    "Access-Control-Allow-Methods": "OPTIONS,POST,GET"
}

logic_flow = """
0: scan for all checkins
1: delete_item one by one
2: ignore inactive checkin for now
"""

def checkout():
    checkins = get_active_checkins()
    for checkin in checkins:
        delete_checkin(checkin.CardReaderID)
    return {
        'statusCode': 200,
        'body': json.dumps([{
            'msg': '{} students checked out successfully'.format(len(checkins)),
            'msgType': 'info'
        }]),
        'headers': headers
    }

def get_active_checkins():
    checkins = dynamodb_client.scan(
        TableName='DigitizeActiveCheckins'
    )['Items']
    checkins = [ActiveCheckin(checkin) for checkin in checkins]
    return checkins

def delete_checkin(cardreaderid):
    response = dynamodb_client.delete_item(
        TableName='DigitizeActiveCheckins',
        Key={'CardReaderID':{'N':str(cardreaderid)}}
    )

# Lambda handler
def handler(event, context):
    return checkout()
