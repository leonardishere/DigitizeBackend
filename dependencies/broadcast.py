import json
import boto3
import os
import sys

client = boto3.client('sns', region_name='us-west-2')

def broadcast(msg, topic):
    print('broadcasting to ', topic)
    response = client.publish(
        TopicArn=topic,
        Message=json.dumps(msg)#,
        #MessageStructure='string',
        #MessageAttributes={
        #    'string': {
        #        'DataType': 'string',
        #        'StringValue': 'string',
        #        'BinaryValue': b'bytes'
        #    }
        #}
    )
    return response
