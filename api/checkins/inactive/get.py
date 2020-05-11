import json
import boto3
import sys
sys.path.append('dependencies') # local location of dependencies
from student import Student
from inactivecheckin import InactiveCheckin

INACTIVE_CHECKINS_TABLE = os.environ['INACTIVE_CHECKINS_TABLE']
dynamodb_client = boto3.client('dynamodb', region_name='us-west-2')

headers = {
    "Content-Type": "application/json",
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Headers": "Content-Type",
    "Access-Control-Allow-Methods": "OPTIONS,GET,POST,PUT,DELETE"
}

def get_inactive_checkins():
    arr = dynamodb_client.scan(TableName='DigitizeInactiveCheckins')['Items']
    arr = [InactiveCheckin(checkin) for checkin in arr]
    arr.sort(key=lambda checkin: -checkin.CheckoutTime)
    data = [checkin.to_dict() for checkin in arr]
    return {
        'statusCode': 200,
        'body': json.dumps(data),
        'headers': headers
    }

# Lambda handler
def handler(event, context):
    try:
        return get_inactive_checkins()
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'Error': str(e)}),
            'headers': headers
        }
