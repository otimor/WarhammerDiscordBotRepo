import json
import requests
import asyncio
#from warhammer_bot.commands import hello
from warhammer_bot import hello, test
import logging as log

import logging


#log.basicConfig(level=log.DEBUG)
log = logging.getLogger()
log.setLevel("DEBUG")
def send_message(WEBHOOK_ID, WEBHOOK_TOKEN, payload):
    headers = {'content-type': 'application/json'}
    url = f'https://discord.com/api/v10/webhooks/{WEBHOOK_ID}/{WEBHOOK_TOKEN}/messages/@original'
    log.info(f"Sending message to discord")
    log.debug(f"Message details, URL: {url}, Payload: {payload}, Headers: {headers}")
    response = requests.patch(url, data=json.dumps(payload), headers=headers)
    log.debug(
        f"Response from discord: {response.status_code} {response.reason} {response.text}"
    )
    return response

def command_handler(event, context):
    log.debug(f"command_handler:Event: {event}, context: {context}")
    str_body = event['Records'][0]['Sns']['Message']  # should be string, for successful sign
    body = json.loads(str_body)

    try:# validate the interaction
        command = body['data']['name']
        WEBHOOK_ID = body['application_id']
        WEBHOOK_TOKEN = body['token']
    except KeyError:
        return {
            'statusCode': 400,
            'body': json.dumps('invalid request')
        }

    try:
        log.info(f"Handling command: {command}")
        payload = command()
        log.debug(f"webhook_id: {WEBHOOK_ID} webhook_token: {WEBHOOK_TOKEN[1:10]} Payload: {payload}")
        response = send_message(WEBHOOK_ID, WEBHOOK_TOKEN, payload)
        return response

    except:
        return {
            'statusCode': 400,
            'body': json.dumps('unhandled command')
        }

