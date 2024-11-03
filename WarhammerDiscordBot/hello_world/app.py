import json

from nacl.signing import VerifyKey
from nacl.exceptions import BadSignatureError

PUBLIC_KEY = '8327fc9706afcfc96f72c1c0010b13e6af4f6d1c3b61dfd48d867270501525ca'


def lambda_handler(event, context):
    #we will convert that
    try:
        body = json.loads(event['body'])

        try:
            signature = event['headers']['x-signature-ed25519']
            timestamp = event['headers']['x-signature-timestamp']
        except KeyError:
            return {
                'statusCode': 401,
                'body': json.dumps('invalid request signature')
            }


        # validate the interaction

        verify_key = VerifyKey(bytes.fromhex(PUBLIC_KEY))

        message = timestamp + event['body']

        try:
            verify_key.verify(message.encode(), signature=bytes.fromhex(signature))
        except BadSignatureError:
            return {
                'statusCode': 401,
                'body': json.dumps('invalid request signature')
            }

        # handle the interaction
        #refactor t to be more readable, wna whta is types?
        t = body['type']

        if t == 1:
            return {
                'statusCode': 200,
                'body': json.dumps({
                    'type': 1
                })
            }
        elif t == 2:
            return command_handler(body)
        else:
            return {
                'statusCode': 400,
                'body': json.dumps('unhandled request type')
            }
    except:
        raise


def command_handler(body):
    command = body['data']['name']

    if command == 'hello':
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
    elif command == 'test':
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
    else:
        return {
            'statusCode': 400,
            'body': json.dumps('unhandled command')
        }