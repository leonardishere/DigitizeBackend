import json
import boto3
import os
import sys
sys.path.append('dependencies') # local location of dependencies
from student import Student

BROADCAST_TOPIC = os.environ['BROADCAST_TOPIC']

table = (boto3
            .resource('dynamodb', region_name='us-west-2')
            .Table('DigitizeStudents')
        )

sns_client = boto3.client('sns', region_name='us-west-2')

headers = {
    "Content-Type": "application/json",
    "Access-Control-Allow-Origin": "*", #"https://digitize.aleonard.dev",
    "Access-Control-Allow-Headers": "Content-Type",
    "Access-Control-Allow-Methods": "OPTIONS,POST,GET"
}

def get_student(cardid):
    try:
        response = dynamodb_client.query(
            TableName='DigitizeStudents',
            KeyConditionExpression="CardID=:cardid",
            ExpressionAttributeValues={
                ":cardid": { "S": cardid }
            },
            ScanIndexForward=True
        )
        return [Student(item) for item in response['Items']]
    except Exception as e:
        return []

def post_student(student):
    try:
        existing_students = get_student(student.CardID)
        if len(existing_students) > 0:
            return {
                'statusCode': 500,
                'body': 'Error: Student already exists',
                'headers': headers
            }
        student = student.to_dict()
        ddb_response = table.put_item(Item=student)
        broadcast_msg = json.dumps({
            'msgType': 'info',
            'msg': 'New Student Added',
            'data': {
                'students_added': [student]
            }
        })
        sns_response = sns_client.publish(
            TopicArn=BROADCAST_TOPIC,
            #TopicArn='arn:aws:sns:us-west-2:917159232232:DigitizeBroadcasts',
            Message=broadcast_msg
        )
        http_response = {
            'statusCode': 200,
            'body': json.dumps({
                'msgType': 'info',
                'msg': 'New Student Added',
                'data': {
                    'students_added': [student]
                }
            }),
            'headers': headers
        }
        return http_response
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({
                'msgType': 'ignore',
                'msg': '',
                'error': str(e)
            }),
            'headers': headers
        }

# Lambda handler
def handler(event, context):
    try:
        student = Student(json.loads(event['body']))
    except Exception as e:
        return {
            'statusCode': 400,
            'body': json.dumps({
                'msgType': 'ignore',
                'msg': '',
                'error': str(e)
            }),
            'headers': headers
        }
    return post_student(student)
