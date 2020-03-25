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
1: delete active checkins one by one
2: batch write inactive checkins
"""

def checkout():
    checkins = get_active_checkins()
    for checkin in checkins:
        delete_active_checkin(checkin['CardReaderID']['N'])
    write_inactive_checkins(checkins)
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
    return checkins

def delete_active_checkin(cardreaderid):
    response = dynamodb_client.delete_item(
        TableName='DigitizeActiveCheckins',
        Key={'CardReaderID':{'N':str(cardreaderid)}}
    )

def write_inactive_checkins(active_checkins):
    if len(active_checkins) == 0:
        return
    curtime = str(int(time()*1000))
    items = list(map(lambda checkin: {
        'PutRequest': {
            'Item': {
                'StudentID': checkin['Student']['M']['StudentID'],
                'Student': checkin['Student'],
                'CardReaderID': {'N': str(checkin['CardReaderID']['N'])},
                'CheckinTime': {'N': str(checkin['CheckinTime']['N'])},
                'CheckoutTime': {'N': curtime}
            }
        }
    }, active_checkins))
    response = dynamodb_client.batch_write_item(
        RequestItems={
            'DigitizeInactiveCheckins': items
        }
    )

# Lambda handler
def handler(event, context):
    try:
        return checkout()
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'Error': str(e)})
            'headers': headers
        }
