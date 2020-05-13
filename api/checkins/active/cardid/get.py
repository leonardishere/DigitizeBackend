import json
import boto3
import os
import sys
sys.path.append('dependencies') # local location of dependencies
from student import Student
from activecheckin import ActiveCheckin

ACTIVE_CHECKINS_TABLE = os.environ['ACTIVE_CHECKINS_TABLE']
dynamodb_client = boto3.client('dynamodb', region_name='us-west-2')

headers = {
    "Content-Type": "application/json",
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Headers": "Content-Type",
    "Access-Control-Allow-Methods": "OPTIONS,GET,POST,PUT,DELETE"
}

def get_active_checkin(cardid):
    try:
        response = dynamodb_client.query(
            TableName=ACTIVE_CHECKINS_TABLE,
            IndexName='CardID',
            KeyConditionExpression="CardID=:cardid",
            ExpressionAttributeValues={
                ":cardid": { "S": cardid }
            },
            ScanIndexForward=True
        )
        if len(response['Items']) == 1:
            checkin = ActiveCheckin(response['Items'][0])
            return {
                'statusCode': 200,
                'body': checkin.to_json(),
                'headers': headers
            }
        elif len(response['Items']) > 1:
            checkins = [ActiveCheckin(checkin).to_dict() for checkin in response['Items']]
            return {
                'statusCode': 500,
                'body': json.dumps({
                    'Error': 'More than one checkin found',
                    'Checkins': checkins
                }),
                'headers': headers
            }
        else:
            return {
                'statusCode': 404,
                'body': json.dumps({'Error': 'Active Checkin with CardID={} not found'.format(cardid)}),
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
        return get_active_checkin(event['pathParameters']['CardID'])
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'Error': str(e)}),
            'headers': headers
        }
