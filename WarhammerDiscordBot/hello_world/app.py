import json

from nacl.signing import VerifyKey
from nacl.exceptions import BadSignatureError

PUBLIC_KEY = '8327fc9706afcfc96f72c1c0010b13e6af4f6d1c3b61dfd48d867270501525ca'
import logging

#log.basicConfig(level=log.DEBUG)
log = logging.getLogger()
log.setLevel("DEBUG")

def lambda_handler(event, context):
    #we will convert that
    log.info(f"Received call to proxyGateway: {event}")
    try:
        body = json.loads(event['body'])

        try:
            signature = event['headers']['x-signature-ed25519']
            timestamp = event['headers']['x-signature-timestamp']
        except KeyError:
            log.warning("Invalid request signature, missing headers ")
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
            log.error("Invalid request signature")
            return {
                'statusCode': 401,
                'body': json.dumps('invalid request signature')
            }

        # handle the interaction
        #refactor t to be more readable, wna whta is types?
        t = body['type']

        if t == 1:
            log.info("Received PING")
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
    log.info(f"Received command: {command}")
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
        log.info("Test command received")
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
        log.warning("Unhandled command received")
        return {
            'statusCode': 400,
            'body': json.dumps('unhandled command')
        }