import json
import boto3
import sys

sys.path.append('dependencies') # local location of dependencies
from student import Student

# initiating the dynamodb client takes >200 ms. moving out here to init once and persist
dynamodb_client = boto3.client('dynamodb', region_name='us-west-2')

headers = {
    "Content-Type": "application/json",
    "Access-Control-Allow-Origin": "https://digitize.aleonard.dev",
    "Access-Control-Allow-Headers": "Content-Type",
    "Access-Control-Allow-Methods": "OPTIONS,POST,GET"
}

def get_students():
    arr = dynamodb_client.scan(
        TableName='DigitizeStudents'
    )['Items']
    arr = [Student(student) for student in arr]
    arr.sort(key=lambda student: student.Name)
    data = [student.to_dict() for student in arr]
    return {'statusCode': 200,
            'body': json.dumps(data),
            'headers': headers}

# Lambda handler
def handler(event, context):
    return get_students()
