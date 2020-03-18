import json
import datetime

def get_handler(event, context):
    data = {
        'output': 'Hello World from GET /',
        'timestamp': datetime.datetime.utcnow().isoformat()
    }
    return {'statusCode': 200,
            'body': json.dumps(data),
            'headers': {'Content-Type': 'application/json'}}

def post_handler(event, context):
    data = {
        'output': 'Hello World from POST /',
        'timestamp': datetime.datetime.utcnow().isoformat()
    }
    return {'statusCode': 200,
            'body': json.dumps(data),
            'headers': {'Content-Type': 'application/json'}}

def default_handler(event, context):
    data = {
        'error': 'Could not handle request {} {}'.format(event['httpMethod'], event['resource'])
    }
    return {'statusCode': 400,
            'body': json.dumps(data),
            'headers': {'Content-Type': 'application/json'}}

def handler(event, context):
    if event['httpMethod'] == "GET" and event['resource'] == "/":
        return get_handler(event, context)
    if event['httpMethod'] == "POST" and event['resource'] == "/":
        return post_handler(event, context)
    return default_handler(event, context)
