import json
import boto3
import os
import sys
sys.path.append('dependencies') # local location of dependencies
from student import Student

STUDENTS_TABLE = os.environ['STUDENTS_TABLE']
dynamodb_client = boto3.client('dynamodb', region_name='us-west-2')

headers = {
    "Content-Type": "application/json",
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Headers": "Content-Type",
    "Access-Control-Allow-Methods": "OPTIONS,GET,POST,PUT,DELETE"
}

def get_students():
    arr = dynamodb_client.scan(TableName=STUDENTS_TABLE)['Items']
    arr = [Student(student) for student in arr]
    arr.sort(key=lambda student: student.Name)
    data = [student.to_dict() for student in arr]
    return {
        'statusCode': 200,
        'body': json.dumps([{
            'msg': 'Received students data',
            'msgType': 'ignore',
            'data': {
                'students': data
            }
        }]),
        'headers': headers
    }

# Lambda handler
def handler(event, context):
    try:
        return get_students()
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'Error': str(e)}),
            'headers': headers
        }
