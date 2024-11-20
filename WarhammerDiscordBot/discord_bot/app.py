import json
import boto3
from auth import DiscordBotAuthorizer
from aws_tools import get_sns_topic_arn, get_secret
import logging

#log.basicConfig(level=log.DEBUG)
log = logging.getLogger()
log.setLevel("DEBUG")
discord_message_types = enumerate(['PING', 'APPLICATION_COMMAND', 'MESSAGE_COMPONENT', 'MESSAGE'])
def check_if_test_call(event):
    if 'x-test' in event['headers'] and event['headers']['x-test'] == 'ping':
        log.info("Test call received")
        return True
    return False

def lambda_handler(event, context):

    try:
        log.info(f"Received call to proxyGateway")
        log.debug(f"Headers: {event['headers']} Event: {event}")
        body = json.loads(event['body'])
        if check_if_test_call(event):
            return {
                'statusCode': 200,
                'body': json.dumps('test successful')
            }
        try:
            public_key = get_secret()
            signature = event['headers']['x-signature-ed25519']
            timestamp = event['headers']['x-signature-timestamp']
            log.debug("Auth begin")
            authorizer = DiscordBotAuthorizer(public_key)
            authenticated, reason = authorizer.validate(signature=signature,
                                                        timestamp=timestamp,
                                                        body=event['body'])

            log.debug(f"Auth end: results: {authenticated},{reason}")

        except KeyError:
            return {
                'statusCode': 401,
                'body': json.dumps('DHBError: invalid request signature')
            }

            # handle the interaction
            # refactor t to be more readable, wna whta is types?

            message_type = body['type']

            if message_type == discord_message_types['PING']: #t == 1:
                log.info("Received ping, reposnding with pong")
                return {
                    'statusCode': 200,
                    'body': json.dumps({
                        'type': 1
                    })
                }
            elif message_type == discord_message_types['APPLICATION_COMMAND']: #t == 2:
                log.info("Processing command received")
                return command_handler(body)
            else:
                return {
                    'statusCode': 400,
                    'body': json.dumps('DHBError: unhandled request type')
                }
    except:
        raise

def command_handler(body):
    # Handle command (send to SNS and split to one of Lambdas)
    if 'name' in body['data']:
        event_text = json.dumps(body, indent=2)
        log.debug(f"Command received: {event_text}")

        params = {
            'Message': event_text,
            'Subject': "Test SNS From Lambda",
            'TopicArn': get_sns_topic_arn(),
            'MessageAttributes': {
                'command': {
                    'DataType': 'String',
                    'StringValue': body['data']['name']
                }
            }
        }
        log.debug(f'Sending message to SNS: {params}')
        # Create promise and SNS service object
        sns = boto3.client('sns', api_version='2010-03-31')
        sns.publish(**params)

        return {
            'statusCode': 200,
            'body': json.dumps({
                "type": 4,
                "data": {"content": "*⏳ Loading...*"}
            })
        }

    return {
        'statusCode': 404
    }
