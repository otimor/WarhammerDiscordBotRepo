import json

def hello():
    return {
        'statusCode': 200,
        'headers': {'Content-Type': 'application/json'},
        'body': json.dumps({
            'type': 4,
            'data': {
                'content': 'Hello, World from CodeCatalyst AWS hello',
            }
        })
    }


def test():
    return {
        'statusCode': 200,
        'headers': {'Content-Type': 'application/json'},
        'body': json.dumps({
            'type': 4,
            'data': {
                'content': 'Test successful',
            }
        })
    }