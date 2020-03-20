import json
import boto3
import sys

sys.path.append('dependencies')
from student import Student

table = (boto3
            .resource('dynamodb', region_name='us-west-2')
            .Table('DigitizeStudents')
        )

headers = {
    "Content-Type": "application/json",
    "Access-Control-Allow-Origin": "https://digitize.aleonard.dev",
    "Access-Control-Allow-Headers": "Content-Type",
    "Access-Control-Allow-Methods": "OPTIONS,POST,GET"
}

def get_student(studentid):
    try:
        response = table.get_item(Key={'StudentID': studentid})
        if 'Item' in response:
            return {'statusCode': 200,
                    'body': json.dumps(response['Item']),
                    'headers': headers}
        else:
            return {'statusCode': 404,
                    'body': json.dumps({'Error': 'Student with StudentID={} not found'.format(studentid)}),
                    'headers': headers}
    except Exception as e:
        return {'statusCode': 500,
                'body': json.dumps({'Error': str(e)}),
                'headers': headers}

# Lambda handler
def handler(event, context):
    return get_student(event['pathParameters']['StudentID'])
