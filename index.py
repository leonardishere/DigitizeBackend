import json
import datetime

def none_handler():
    data = {
        'need to': 'change test case',
        'or': 'my "server" code',
        'until then': 'Hello World'
    }
    return {'statusCode': 200,
            'body': json.dumps(data),
            'headers': {'Content-Type': 'application/json'}}

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
    if event is None and context is None:
        return none_handler()
    if event['httpMethod'] == "GET" and event['resource'] == "/":
        return get_handler(event, context)
    if event['httpMethod'] == "POST" and event['resource'] == "/":
        return post_handler(event, context)
    return default_handler(event, context)
