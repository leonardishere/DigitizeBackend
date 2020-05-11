import json
import boto3
import sys
sys.path.append('dependencies')
from student import Student

STUDENTS_TABLE = os.environ['STUDENTS_TABLE']
dynamodb_client = boto3.client('dynamodb', region_name='us-west-2')

headers = {
    "Content-Type": "application/json",
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Headers": "Content-Type",
    "Access-Control-Allow-Methods": "OPTIONS,GET,POST,PUT,DELETE"
}

def get_student(studentid):
    try:
        response = dynamodb_client.query(
            TableName=STUDENTS_TABLE,
            IndexName='StudentID',
            KeyConditionExpression="StudentID=:studentid",
            ExpressionAttributeValues={
                ":studentid": { "S": studentid }
            },
            ScanIndexForward=True
        )
        if len(response['Items']) == 1:
            student = Student(response['Items'][0])
            return {
                'statusCode': 200,
                'body': student.to_json(),
                'headers': headers
            }
        elif len(response['Items']) > 1:
            students = [Student(student).to_dict() for student in response['Items']]
            return {
                'statusCode': 500,
                'body': json.dumps({
                    'Error': 'More than one student found',
                    'Students': students
                }),
                'headers': headers
            }
        else:
            return {
                'statusCode': 404,
                'body': json.dumps({'Error': 'Student with StudentID={} not found'.format(cardid)}),
                'headers': headers
            }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'Error': str(e)}),
            'headers': headers
        }

# Lambda handler
def handler(event, context):
    try:
        return get_student(event['pathParameters']['StudentID'])
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'Error': str(e)}),
            'headers': headers
        }
