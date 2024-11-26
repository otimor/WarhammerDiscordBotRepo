import json
import logging


def hello():
    return 'Hello, World from CodeCatalyst AWS hello'



def test():
    logging.debug("Generating test result command")
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