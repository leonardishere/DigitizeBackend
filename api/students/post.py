import json
import boto3
import sys

sys.path.append('dependencies') # local location of dependencies
from student import Student

table = (boto3
            .resource('dynamodb', region_name='us-west-2')
            .Table('DigitizeStudents')
        )

headers = {
    "Content-Type": "application/json",
    "Access-Control-Allow-Origin": "*", #"https://digitize.aleonard.dev",
    "Access-Control-Allow-Headers": "Content-Type",
    "Access-Control-Allow-Methods": "OPTIONS,POST,GET"
}

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
    try:
        student = Student(json.loads(event['body']))
    except Exception as e:
        return {'statusCode': 400,
                'body': {'Error': str(e)},
                'headers': headers}
    return post_student(student)
