import json
import boto3
import os
import sys
import traceback
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

# logic flow:
# HTTP request contains CardReaderID, CardID
# 0: get active checkin by CardReaderID
# 1: get active checkin by CardID
# 2: if CardID is already checked in to CardReaderID (ref 0,1), exit
# - only one is required to make this assertion, not both
# 3: get student by CardID
# 4: checkout 1 and 2 if they exist
# - delete active checkin, create inactivecheckin for both
# 5: checkin CardID at CardReaderID
# - 4 and 5 need to happen anotomically (total of 1, 3, or 5 writes)


def checkin(cardreaderid, cardid):
    # 0: get active checkin by CardReaderID
    checkins1 = get_active_checkins_by_cardreaderid(cardreaderid)
    # 2: if CardID is already checked into CardReaderID, exit
    if len(checkins1) > 0 and checkins1[0]['CardID']['S'] == cardid:
        return {
            'statusCode': 200,
            'body': json.dumps([{
                'msg': 'Redundant Checkin',
                'msgType': 'ignore'
            }]),
            'headers': headers
        }
    # 1: get active checkin by CardID
    checkins2 = get_active_checkins_by_cardid(cardid)
    # 3: get student by CardID
    students = get_student_by_cardid(cardid)
    if len(students) == 0:
        return {
            'statusCode': 404,
            'body': json.dumps([{
                'msg': 'Student not found',
                'msgType': 'error'
            }]),
            'headers': headers
        }
    student = students[0]
    # 4: checkout 0 if it exists
    TransactItems = []
    successBody = []
    if len(checkins1) > 0:
        successBody.append({
            'msg': '{} checked out'.format(checkins1[0]['Student']['M']['Name']['S']),
            'msgType': 'info',
            'data': {
                'checkout': {
                    'CardReaderID': int(checkins1[0]['CardReaderID']['N']),
                    'CheckoutTime': int(time()*1000)
                }
            }
        })
    if len(checkins2) > 0:
        successBody.append({
            'msg': "{} moved to cardreader {}".format(student['Name']['S'],cardreaderid),
            'msgType': 'info',
            'data': {
                'move': {
                    'OldCardReaderID': int(checkins2[0]['CardReaderID']['N']),
                    'NewCardReaderID': int(cardreaderid)
                }
            }
        })
        TransactItems.append({
            'Delete':{
                'TableName':ACTIVE_CHECKINS_TABLE,
                'Key':{
                    'CardReaderID':{'N':str(checkins2[0]['CardReaderID']['N'])}
                }
            }
        })
    else:
        successBody.append({
            'msg':"{} checked in at cardreader {}".format(student['Name']['S'],cardreaderid),
            'msgType': 'info',
            'data': {
                'checkin': {
                    'CardReaderID': int(cardreaderid),
                    'CardID'      : cardid,
                    'CheckinTime' : int(time()*1000),
                    'Student'     : {
                        'Name'      : student['Name']['S'],
                        'StudentID' : student['StudentID']['S'],
                        'CardID'    : student['CardID']['S']
                    }
                }
            }
        })
    # 5: checkin CardID at CardReaderID
    checkinTime = int(checkins2[0]['CheckinTime']['N']) if len(checkins2) > 0 else int(time()*1000)
    TransactItems.append({
        'Put':{
            'TableName':ACTIVE_CHECKINS_TABLE,
            'Item':{
                'CardReaderID': {'N': str(cardreaderid)},
                'CardID'      : {'S': student['CardID']['S']},
                'CheckinTime' : {'N': str(checkinTime)},
                'Student'     : {'M': student}
            }
        }
    })
    # 4 and 5 atomically
    # well I guess you can't atomically write across multiple tables
    res = dynamodb_client.transact_write_items(TransactItems=TransactItems)
    if len(checkins1) > 0:
        res2 = write_inactive_checkin(checkins1[0])
    successBody = json.dumps(successBody)
    sns_response = sns_client.publish(
        TopicArn=BROADCAST_TOPIC,
        Message=successBody
    )
    return {
        'statusCode': 200,
        'body': successBody,
        'headers': headers
    }

def get_active_checkins_by_cardreaderid(cardreaderid):
    response = dynamodb_client.query(
        TableName=ACTIVE_CHECKINS_TABLE,
        KeyConditionExpression="CardReaderID=:cardreaderid",
        ExpressionAttributeValues={
            ":cardreaderid": { "N": cardreaderid }
        },
        ScanIndexForward=True
    )
    return response['Items']

def get_active_checkins_by_cardid(cardid):
    response = dynamodb_client.query(
        TableName=ACTIVE_CHECKINS_TABLE,
        IndexName='CardID',
        KeyConditionExpression="CardID=:cardid",
        ExpressionAttributeValues={
            ":cardid": { "S": cardid }
        },
        ScanIndexForward=True
    )
    return response['Items']

def get_student_by_cardid(cardid):
    response = dynamodb_client.query(
        TableName=STUDENTS_TABLE,
        KeyConditionExpression="CardID=:cardid",
        ExpressionAttributeValues={
            ":cardid": { "S": cardid }
        },
        ScanIndexForward=True
    )
    return response['Items']

def write_inactive_checkin(active_checkin):
    curtime = str(int(time()*1000))
    inactive_checkin = {
        'StudentID': active_checkin['Student']['M']['StudentID'],
        'Student': active_checkin['Student'],
        'CardReaderID': {'N': str(active_checkin['CardReaderID']['N'])},
        'CheckinTime': {'N': str(active_checkin['CheckinTime']['N'])},
        'CheckoutTime': {'N': curtime}
    }
    response = dynamodb_client.put_item(
        TableName=INACTIVE_CHECKINS_TABLE,
        Item=inactive_checkin
    )

# Lambda handler
def handler(event, context):
    try:
        if not event or not 'body' in event or not event['body']:
            return {
                'statusCode': 400,
                'body': '{"Error": "No event body"}',
                'headers': headers
            }
        req = json.loads(event['body'])
        if 'CardReaderID' not in req or 'CardID' not in req:
            return {
                'statusCode': 400,
                'body': '{"Error": "Required parameters: CardReaderID, CardID"}',
                'headers': headers
            }
        cardreaderid = str(req['CardReaderID'])
        cardid = req['CardID']
        return checkin(cardreaderid, cardid)
    except Exception as e:
        traceback.print_exc()
        return {
            'statusCode': 500,
            'body': json.dumps({'Error': str(e)}),
            'headers': headers
        }
