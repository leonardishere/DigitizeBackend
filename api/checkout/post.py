import json
import boto3
import os
import sys
from time import time
sys.path.append('dependencies') # local location of dependencies
from student import Student
from activecheckin import ActiveCheckin

STUDENTS_TABLE = os.environ['STUDENTS_TABLE']
ACTIVE_CHECKINS_TABLE = os.environ['ACTIVE_CHECKINS_TABLE']
INACTIVE_CHECKINS_TABLE = os.environ['INACTIVE_CHECKINS_TABLE']
dynamodb_client = boto3.client('dynamodb', region_name='us-west-2')
BROADCAST_TOPIC = os.environ['BROADCAST_TOPIC']
sns_client = boto3.client('sns', region_name='us-west-2')

headers = {
    "Content-Type": "application/json",
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Headers": "Content-Type",
    "Access-Control-Allow-Methods": "OPTIONS,GET,POST,PUT,DELETE"
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
    msg = json.dumps([{
        'msg': 'Class dismissed',
        'msgType': 'info'
    }])
    sns_response = sns_client.publish(
        TopicArn=BROADCAST_TOPIC,
        Message=msg
    )
    return {
        'statusCode': 200,
        'body': msg,
        'headers': headers
    }

def get_active_checkins():
    checkins = dynamodb_client.scan(TableName=ACTIVE_CHECKINS_TABLE)['Items']
    return checkins

def delete_active_checkin(cardreaderid):
    response = dynamodb_client.delete_item(
        TableName=ACTIVE_CHECKINS_TABLE,
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
        RequestItems={INACTIVE_CHECKINS_TABLE: items})

# Lambda handler
def handler(event, context):
    try:
        return checkout()
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'Error': str(e)}),
            'headers': headers
        }
