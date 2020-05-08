import json
import boto3
import os
import sys
sys.path.append('dependencies') # local location of dependencies
from student import Student
#from broadcast import broadcast

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

def post_student(student):
    try:
        print('here 1')
        student = student.to_dict()
        print('here 2')
        ddb_response = table.put_item(Item=student)
        print('here 3')
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
        broadcast_msg = json.dumps({
            'msgType': 'info',
            'msg': 'New Student Added',
            'data': {
                'students_added': [student]
            }
        })
        print('here 4')
        #broad_res = broadcast(msg, BROADCAST_TOPIC)
        print('broadcasting to ', BROADCAST_TOPIC)
        broad_res = sns_client.publish(
            TopicArn=BROADCAST_TOPIC,
            #TopicArn='arn:aws:sns:us-west-2:917159232232:DigitizeBroadcasts',
            Message=broadcast_msg
        )
        print('here 5')
        print(broad_res)
        print('here 6')
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
        #eventbody = json.loads(event['body'])
        #print('event body:', json.dumps(eventbody, indent=2))
        student = Student(json.loads(event['body']))
        print('student:', student)
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
