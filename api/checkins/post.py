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
HTTP request contains CardReaderID, CardID
0: get active checkin by CardReaderID
1: get active checkin by CardID
2: if CardID is already checked in to CardReaderID (ref 0,1), exit
- only one is required to make this assertion, not both
3: get student by CardID
4: checkout 1 and 2 if they exist
- delete active checkin, create inactivecheckin for both
5: checkin CardID at CardReaderID
- 4 and 5 need to happen anotomically (total of 1, 3, or 5 writes)
"""

def checkin(cardreaderid, cardid):
    # 0: get active checkin by CardReaderID
    checkins1 = get_active_checkins_by_cardreaderid(cardreaderid)
    # 2: if CardID is already checked into CardReaderID, exit
    if len(checkins1) > 0 and checkins1[0].CardID == cardid:
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
            'msg': '{} checked out'.format(checkins1[0].Student.Name),
            'msgType': 'info'
        })
    if len(checkins2) > 0:
        successBody.append({
            'msg': "{} moved to cardreader {}".format(student.Name,cardreaderid),
            'msgType': 'info'
        })
        TransactItems.append({
            'Delete':{
                'TableName':'DigitizeActiveCheckins',
                'Key':{
                    'CardReaderID':{'N':str(checkins2[0].CardReaderID)}
                }
            }
        })
    else:
        successBody.append({
            'msg':"{} checked in at cardreader {}".format(student.Name,cardreaderid),
            'msgType': 'info'
        })
    # 5: checkin CardID at CardReaderID
    checkinTime = checkins2[0].CheckinTime if len(checkins2) > 0 else int(time())
    TransactItems.append({
        'Put':{
            'TableName':'DigitizeActiveCheckins',
            'Item':{
                'CardReaderID': {'N': str(cardreaderid)},
                'CardID'   : {'S': student.CardID},
                'CheckinTime' : {'N': str(checkinTime)},
                'Student'     : {'M': student.item}
            }
        }
    })
    # 4 and 5 atomically
    res = dynamodb_client.transact_write_items(TransactItems=TransactItems)
    if res['ResponseMetadata']['HTTPStatusCode'] == 200:
        return {
            'statusCode': 200,
            'body': json.dumps(successBody),
            'headers': headers
        }
    else:
        return {
            'statusCode': res['ResponseMetadata']['HTTPStatusCode'],
            'body': json.dumps([{
                'msg': res,
                'msgType': 'error'
            }]),
            'headers': headers
        }

def get_active_checkins_by_cardreaderid(cardreaderid):
    response = dynamodb_client.query(
        TableName='DigitizeActiveCheckins',
        KeyConditionExpression="CardReaderID=:cardreaderid",
        ExpressionAttributeValues={
            ":cardreaderid": { "N": cardreaderid }
        },
        ScanIndexForward=True
    )
    return [ActiveCheckin(checkin) for checkin in response['Items']]

def get_active_checkins_by_cardid(cardid):
    response = dynamodb_client.query(
        TableName='DigitizeActiveCheckins',
        IndexName='CardID',
        KeyConditionExpression="CardID=:cardid",
        ExpressionAttributeValues={
            ":cardid": { "S": cardid }
        },
        ScanIndexForward=True
    )
    return [ActiveCheckin(checkin) for checkin in response['Items']]

def get_student_by_cardid(cardid):
    response = dynamodb_client.query(
        TableName='DigitizeStudents',
        KeyConditionExpression="CardID=:cardid",
        ExpressionAttributeValues={
            ":cardid": { "S": cardid }
        },
        ScanIndexForward=True
    )
    return [Student(student) for student in response['Items']]

def post_student(student):
    try:
        student = student.to_dict()
        response = table.put_item(Item=student)
        return {'statusCode': 200,
                'body': '',
                'headers': headers}
    except Exception as e:
        return {'statusCode': 500,
                'body': {'Error': str(e)},
                'headers': headers}

# Lambda handler
def handler(event, context):
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
