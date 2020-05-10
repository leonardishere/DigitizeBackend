import json
import boto3
import os
import sys
sys.path.append('dependencies') # local location of dependencies
from student import Student

BROADCAST_TOPIC = os.environ['BROADCAST_TOPIC']
dynamodb_client = boto3.client('dynamodb', region_name='us-west-2')
sns_client = boto3.client('sns', region_name='us-west-2')

headers = {
    "Content-Type": "application/json",
    "Access-Control-Allow-Origin": "*", #"https://digitize.aleonard.dev",
    "Access-Control-Allow-Headers": "Content-Type",
    "Access-Control-Allow-Methods": "OPTIONS,POST,GET"
}

def post_student(student):
    # parse student
    try:
        student = Student(json.loads(student))
        student_item = student.to_dynamo_item()
    except Exception as e:
        return {
            'statusCode': 400,
            'body': "Error: Could not parse request.",
            'headers': headers
        }

    # update dynamodb
    try:
        dynamo_response = dynamodb_client.put_item(
            TableName='DigitizeStudents',
            Item=student_item,
            ConditionExpression='attribute_not_exists(CardID) AND attribute_not_exists(StudentID)'
        )
    except Exception as e:
        return {
            'statusCode': 400,
            'body': "Error: Student already exists.",
            'headers': headers
        }

    # broadcast
    try:
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
    except Exception as e:
        return {
            'statusCode': 500,
            'body': "Error: Could not broadcast.",
            'headers': headers
        }

    # success
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

# Lambda handler
def handler(event, context):
    return post_student(event['body'])
