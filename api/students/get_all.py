import json
import boto3
import os
import sys
sys.path.append(os.path.join(os.curdir, "entities"))
from student import Student

#from aws_xray_sdk.core import xray_recorder
#from aws_xray_sdk.core import patch_all
#xray_recorder.configure(context_missing='LOG_ERROR')
#patch_all()

# initiating the dynamodb client takes >200 ms. moving out here to init once and persist
dynamodb_client = boto3.client('dynamodb', region_name='us-west-2')

def get_students():
    arr = dynamodb_client.scan(
        TableName='DigitizeStudents'
    )['Items']
    arr = [Student(student) for student in arr]
    arr.sort(key=lambda student: student.Name)
    data = [student.to_json() for student in arr]
    return {'statusCode': 200,
            'body': json.dumps(data),
            'headers': {'Content-Type': 'application/json'}}

# Lambda handler
def handler(event, context):
    return get_students()
