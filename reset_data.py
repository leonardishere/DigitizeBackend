import json
import boto3
import os
import sys
sys.path.append('dependencies') # local location of dependencies
from student import Student

STUDENTS_TABLE = 'DigitizeStudents' #os.environ['STUDENTS_TABLE']
ACTIVE_CHECKINS_TABLE = 'DigitizeActiveCheckins' # os.environ['ACTIVE_CHECKINS_TABLE']
INACTIVE_CHECKINS_TABLE = 'DigitizeInactiveCheckins' # os.environ['INACTIVE_CHECKINS_TABLE']
dynamodb_client = boto3.client('dynamodb', region_name='us-west-2')
dynamodb_resource = boto3.resource('dynamodb', region_name='us-west-2')
BROADCAST_TOPIC = 'arn:aws:sns:us-west-2:917159232232:DigitizeBroadcasts' #os.environ['BROADCAST_TOPIC']
sns_client = boto3.client('sns', region_name='us-west-2')

# ----- Fix Students Begin -----

# create new students
new_students = [
  {"Name": "Adam",     "StudentID": "00001172842", "CardID": "6F2A8C1CE19EBE29"},
  {"Name": "Aubrie",   "StudentID": "00001314509", "CardID": "F703B301F64D8C71"},
  {"Name": "Bailey",   "StudentID": "00001922971", "CardID": "50A23294CF0A7C4F"},
  {"Name": "Barbara",  "StudentID": "00001116739", "CardID": "EE3180C00C9D669B"},
  {"Name": "Caitlyn",  "StudentID": "00001943050", "CardID": "04E794029FEBE26A"},
  {"Name": "Callahan", "StudentID": "00001885421", "CardID": "FBF7A0A30D7544C4"},
  {"Name": "Denise",   "StudentID": "00001153701", "CardID": "C1E3993D55EAF05C"},
  {"Name": "Doug",     "StudentID": "00001469637", "CardID": "B7D0D6B5471E3F09"},
  {"Name": "Elaine",   "StudentID": "00001171835", "CardID": "54795CB806B7110E"},
  {"Name": "Elliot",   "StudentID": "00001581830", "CardID": "C3F0467DDB8BF5AC"},
  {"Name": "Fiona",    "StudentID": "00001536285", "CardID": "B1926EA64CCE3808"},
  {"Name": "Frank",    "StudentID": "00001842243", "CardID": "8526ACF3F411AE95"},
  {"Name": "Gabby",    "StudentID": "00001334355", "CardID": "5458CD3BB4652F28"},
  {"Name": "Gary",     "StudentID": "00001613813", "CardID": "1AE0F9EDE6638344"},
  {"Name": "Heidi",    "StudentID": "00001884110", "CardID": "194EA9F65816BDDE"},
  {"Name": "Henry",    "StudentID": "00001458020", "CardID": "3B656D63D50CFF14"},
  {"Name": "Isabella", "StudentID": "00001839155", "CardID": "3B1C27A0D4F02B88"},
  {"Name": "Isiah",    "StudentID": "00001087466", "CardID": "E64C6B7C9C9A01B4"},
  {"Name": "Jake",     "StudentID": "00001766829", "CardID": "959DEEBD9318AB12"},
  {"Name": "Janice",   "StudentID": "00001388358", "CardID": "52E27AFE2FA65C1C"},
  {"Name": "Kathy",    "StudentID": "00001218726", "CardID": "F7E3E1B6601DB6D2"},
  {"Name": "Kyle",     "StudentID": "00001429504", "CardID": "2B0C19BBFA45D565"},
  {"Name": "Laura",    "StudentID": "00001422925", "CardID": "9F762625C6B49A41"},
  {"Name": "Luke",     "StudentID": "00001852661", "CardID": "50AB1B54A28BECF1"},
  {"Name": "Mary",     "StudentID": "00001954449", "CardID": "E23B0B1D8109E33B"},
  {"Name": "Mike",     "StudentID": "00001940108", "CardID": "2715ECC69997FC57"},
  {"Name": "Nancy",    "StudentID": "00001599568", "CardID": "9A65C902311EF3D2"},
  {"Name": "Nick",     "StudentID": "00001525875", "CardID": "9F4FBBFD55E9FC00"},
  {"Name": "Olivia",   "StudentID": "00001823181", "CardID": "DB594FD88C12756E"},
  {"Name": "Oscar",    "StudentID": "00001137065", "CardID": "A1AC1A7B3C70ECB4"},
  {"Name": "Pablo",    "StudentID": "00001247742", "CardID": "88DB24105B791040"},
  {"Name": "Patty",    "StudentID": "00001812124", "CardID": "1762B6F6D19DD335"},
  {"Name": "Qing",     "StudentID": "00001967910", "CardID": "68622D0CCC0B13A0"},
  {"Name": "Quintin",  "StudentID": "00001896360", "CardID": "5C2CE13F75D9CBCA"},
  {"Name": "Raquel",   "StudentID": "00001947228", "CardID": "F13DBE75791A9140"},
  {"Name": "Ron",      "StudentID": "00001278453", "CardID": "C5BF20E8EF89634D"},
  {"Name": "Samantha", "StudentID": "00001145948", "CardID": "1120EB45AAFFF211"},
  {"Name": "Samuel",   "StudentID": "00001366314", "CardID": "27CF0996557F8A02"},
  {"Name": "Tammy",    "StudentID": "00001527440", "CardID": "6181812E76A41DBC"},
  {"Name": "Thomas",   "StudentID": "00001469283", "CardID": "E557AAEFF170327F"},
  {"Name": "Ulysses",  "StudentID": "00001398541", "CardID": "D258B2C24EB51CDC"},
  {"Name": "Uriel",    "StudentID": "00001004246", "CardID": "86DD7AEA9BF2C65E"},
  {"Name": "Victor",   "StudentID": "00001972686", "CardID": "A9FA700B54999F9E"},
  {"Name": "Victoria", "StudentID": "00001435629", "CardID": "318466287CC93F6E"},
  {"Name": "Wendy",    "StudentID": "00001864389", "CardID": "38D3C06CC23ABCCE"},
  {"Name": "William",  "StudentID": "00001415409", "CardID": "3D12DF41831E4E73"},
  {"Name": "Xandra",   "StudentID": "00001351462", "CardID": "B28C5335764144D2"},
  {"Name": "Xavier",   "StudentID": "00001629931", "CardID": "A27E16A76114D0E1"},
  {"Name": "Yahtzee",  "StudentID": "00001816897", "CardID": "3427DC2CB4EBDD2B"},
  {"Name": "Yvonne",   "StudentID": "00001086384", "CardID": "164D7983F5EED188"},
  {"Name": "Zack",     "StudentID": "00001134788", "CardID": "61E2D81052E52550"},
  {"Name": "Zendaya",  "StudentID": "00001218612", "CardID": "1557A45690BC2C0E"}
]

# get current students
current_students = dynamodb_client.scan(
    TableName=STUDENTS_TABLE,
    Select="SPECIFIC_ATTRIBUTES",
    ProjectionExpression="CardID"
)['Items']

# create requests
delete_requests = list(map(lambda student: {'DeleteRequest':{'Key':{'CardID':student['CardID']['S']}}}, current_students))
put_requests = list(map(lambda student: {'PutRequest':{'Item':student}}, new_students))

# batch write requests
for i in range(0, len(delete_requests), 25):
    batch_requests = delete_requests[i:min(len(delete_requests), i+25)]
    dynamodb_resource.batch_write_item(
        RequestItems={STUDENTS_TABLE: batch_requests}
    )
for i in range(0, len(put_requests), 25):
    batch_requests = put_requests[i:min(len(put_requests), i+25)]
    dynamodb_resource.batch_write_item(
        RequestItems={STUDENTS_TABLE: batch_requests}
    )

# broadcast updates
broadcast_msg = json.dumps([{
    'msgType': 'info',
    'msg': 'New Students Added',
    'data': {
        'students_added': new_students
    }
}])
sns_response = sns_client.publish(
    TopicArn=BROADCAST_TOPIC,
    Message=broadcast_msg
)

# ----- Fix Students End -----
# ----- Fix Active Checkins Begin -----

# create new active checkins
new_active_checkins = [
  {"CardReaderID":  2, "CardID": "E64C6B7C9C9A01B4", "CheckinTime": 1598544664495, "Student": {"Name": "Isiah", "StudentID": "00001087466", "CardID": "E64C6B7C9C9A01B4"}},
  {"CardReaderID":  5, "CardID": "318466287CC93F6E", "CheckinTime": 1598544479724, "Student": {"Name": "Victoria", "StudentID": "00001435629", "CardID": "318466287CC93F6E"}},
  {"CardReaderID": 10, "CardID": "9F4FBBFD55E9FC00", "CheckinTime": 1598544628056, "Student": {"Name": "Nick", "StudentID": "00001525875", "CardID": "9F4FBBFD55E9FC00"}},
  {"CardReaderID": 13, "CardID": "50AB1B54A28BECF1", "CheckinTime": 1598545561266, "Student": {"Name": "Luke", "StudentID": "00001852661", "CardID": "50AB1B54A28BECF1"}},
  {"CardReaderID": 16, "CardID": "3B656D63D50CFF14", "CheckinTime": 1598544938875, "Student": {"Name": "Henry", "StudentID": "00001458020", "CardID": "3B656D63D50CFF14"}},
  {"CardReaderID": 20, "CardID": "C3F0467DDB8BF5AC", "CheckinTime": 1598544549339, "Student": {"Name": "Elliot", "StudentID": "00001581830", "CardID": "C3F0467DDB8BF5AC"}},
  {"CardReaderID": 24, "CardID": "F13DBE75791A9140", "CheckinTime": 1598545058160, "Student": {"Name": "Raquel", "StudentID": "00001947228", "CardID": "F13DBE75791A9140"}},
  {"CardReaderID": 25, "CardID": "1120EB45AAFFF211", "CheckinTime": 1598545074562, "Student": {"Name": "Samantha", "StudentID": "00001145948", "CardID": "1120EB45AAFFF211"}},
  {"CardReaderID": 27, "CardID": "61E2D81052E52550", "CheckinTime": 1598544363615, "Student": {"Name": "Zack", "StudentID": "00001134788", "CardID": "61E2D81052E52550"}},
  {"CardReaderID": 28, "CardID": "A1AC1A7B3C70ECB4", "CheckinTime": 1598545212662, "Student": {"Name": "Oscar", "StudentID": "00001137065", "CardID": "A1AC1A7B3C70ECB4"}},
  {"CardReaderID": 33, "CardID": "86DD7AEA9BF2C65E", "CheckinTime": 1598544808352, "Student": {"Name": "Uriel", "StudentID": "00001004246", "CardID": "86DD7AEA9BF2C65E"}},
  {"CardReaderID": 37, "CardID": "04E794029FEBE26A", "CheckinTime": 1598544908419, "Student": {"Name": "Caitlyn", "StudentID": "00001943050", "CardID": "04E794029FEBE26A"}},
  {"CardReaderID": 40, "CardID": "F703B301F64D8C71", "CheckinTime": 1598545687892, "Student": {"Name": "Aubrie", "StudentID": "00001314509", "CardID": "F703B301F64D8C71"}},
  {"CardReaderID": 41, "CardID": "2715ECC69997FC57", "CheckinTime": 1598544912627, "Student": {"Name": "Mike", "StudentID": "00001940108", "CardID": "2715ECC69997FC57"}},
  {"CardReaderID": 44, "CardID": "5C2CE13F75D9CBCA", "CheckinTime": 1598544822830, "Student": {"Name": "Quintin", "StudentID": "00001896360", "CardID": "5C2CE13F75D9CBCA"}},
  {"CardReaderID": 50, "CardID": "6F2A8C1CE19EBE29", "CheckinTime": 1598544774672, "Student": {"Name": "Adam", "StudentID": "00001172842", "CardID": "6F2A8C1CE19EBE29"}}
]

# get current active checkins
current_active_checkins = dynamodb_client.scan(
    TableName=ACTIVE_CHECKINS_TABLE,
    Select="SPECIFIC_ATTRIBUTES",
    ProjectionExpression="CardReaderID"
)['Items']

# create requests
delete_requests = list(map(lambda checkin: {'DeleteRequest':{'Key':{'CardReaderID':int(checkin['CardReaderID']['N'])}}}, current_active_checkins))
put_requests = list(map(lambda checkin: {'PutRequest':{'Item':checkin}}, new_active_checkins))

# batch write requests
for i in range(0, len(delete_requests), 25):
    batch_requests = delete_requests[i:min(len(delete_requests), i+25)]
    dynamodb_resource.batch_write_item(
        RequestItems={ACTIVE_CHECKINS_TABLE: batch_requests}
    )
for i in range(0, len(put_requests), 25):
    batch_requests = put_requests[i:min(len(put_requests), i+25)]
    dynamodb_resource.batch_write_item(
        RequestItems={ACTIVE_CHECKINS_TABLE: batch_requests}
    )

# broadcast updates
broadcast_msg = json.dumps([{
    'msgType': 'info',
    'msg': 'New Students Checked In',
    'data': {
        'students_added': new_active_checkins
    }
}])
sns_response = sns_client.publish(
    TopicArn=BROADCAST_TOPIC,
    Message=broadcast_msg
)

# ----- Fix Active Checkins Eng -----
# ----- Ignore Inactive Checkins -----
