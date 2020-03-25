import json
import boto3
import sys

sys.path.append('dependencies') # local location of dependencies
from student import Student
from activecheckin import ActiveCheckin

# initiating the dynamodb client takes >200 ms. moving out here to init once and persist
dynamodb_client = boto3.client('dynamodb', region_name='us-west-2')

headers = {
    "Content-Type": "application/json",
    "Access-Control-Allow-Origin": "*", #"https://digitize.aleonard.dev",
    "Access-Control-Allow-Headers": "Content-Type",
    "Access-Control-Allow-Methods": "OPTIONS,POST,GET"
}

def get_active_checkin(cardid):
    try:
        response = dynamodb_client.query(
            TableName='DigitizeActiveCheckins',
            IndexName='CardID',
            KeyConditionExpression="CardID=:cardid",
            ExpressionAttributeValues={
                ":cardid": { "S": cardid }
            },
            ScanIndexForward=True
        )
        if len(response['Items']) == 1:
            checkin = ActiveCheckin(response['Items'][0])
            return {'statusCode': 200,
                    'body': checkin.to_json(),
                    'headers': headers}
        elif len(response['Items']) > 1:
            checkins = [ActiveCheckin(checkin).to_dict() for checkin in response['Items']]
            return {'statusCode': 500,
                    'body': json.dumps({
                        'Error': 'More than one checkin found',
                        'Checkins': checkins
                    }),
                    'headers': headers}
        else:
            return {'statusCode': 404,
                    'body': json.dumps({'Error': 'Active Checkin with CardID={} not found'.format(cardid)}),
                    'headers': headers}
    except Exception as e:
        return {'statusCode': 500,
                'body': json.dumps({'Error': str(e)}),
                'headers': headers}

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
