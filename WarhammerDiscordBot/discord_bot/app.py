import json
import boto3
from auth import DiscordBotAuthorizer, check_auth
from aws_tools import get_sns_topic_arn, get_secret
import logging


#log.basicConfig(level=log.DEBUG)
log = logging.getLogger()
log.setLevel("DEBUG")
discord_message_types = {'PING':1,
                         'APPLICATION_COMMAND':2,
                         'MESSAGE_COMPONENT':3,
                         'MESSAGE':4,
                         'PONG':1}
def build_response(status_code, body):
    headers = { 'Access-Control-Allow-Headers': 'Content-Type',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'POST, GET'}
    headers = ''
    response = {
        'statusCode': status_code,
        'body': json.dumps(body),
        'headers': headers
    }
    return response

basic_response = """{'headers': {
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'POST, GET'
            }"""
def check_if_test_call(event):
    if 'x-test' in event['headers'] and event['headers']['x-test'] == 'ping':
        log.info("Test call received")
        return True
    return False

def lambda_handler(event, context):

    try:
        log.info(f"Received call to proxyGateway")
        log.debug(f"Headers: {event['headers']} Event: {event}")

        if check_if_test_call(event):
            return build_response(200, 'test successful')

        try:
            public_key = get_secret()
            signature = event['headers']['x-signature-ed25519']
            timestamp = event['headers']['x-signature-timestamp']
            body = json.loads(event['body'])
            log.debug("Auth begin")
            #authorizer = DiscordBotAuthorizer(public_key)
            #authenticated, reason = authorizer.validate(signature=signature, timestamp=timestamp, body=event['body'])
            authenticated, reason = check_auth(public_key, signature, timestamp=timestamp, body=event['body'])

            log.debug(f"Auth end: results: {authenticated},{reason}")

        except KeyError:
            log.error("Invalid request signature, missing headers")
            return build_response(401, 'DHBError: invalid request signature')

        # handle the interaction
        message_type = body['type']
        log.debug(f"Processing message type: {message_type}")
        if message_type == discord_message_types['PING']: #t == 1:
            log.info("Received ping, responding with pong")
            return build_response(200, "{'type': discord_message_types['PONG']}")
        elif message_type == discord_message_types['APPLICATION_COMMAND']: #t == 2:
            log.info("Processing command received")
            return command_handler(body)
        else:
            log.error(f"Unhandled request type: {message_type}")
            return build_response(400, 'DHBError: unhandled request type')
    except:
        raise

def command_handler(body):
    # Handle command (send to SNS and split to one of Lambdas)
    if 'name' in body['data']:
        event_text = json.dumps(body, indent=2)
        log.debug(f"Command received: {body['data']['name']}")
        # sns_topic_arn = get_sns_topic_arn()
        sns_topic_arn = 'arn:aws:sns:us-west-2:205930619414:MainSNSTopicName'
        params = {
            'Message': event_text,
            'Subject': "Test SNS From Lambda",
            'TopicArn': sns_topic_arn,
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
                "type": discord_message_types['MESSAGE'],
                "data": {"content": "*⏳ Loading...*"}
            })
        }

    return {
        'statusCode': 404
    }
