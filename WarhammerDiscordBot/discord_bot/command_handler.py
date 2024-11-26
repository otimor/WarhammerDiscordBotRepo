import json
import requests
import asyncio
#from warhammer_bot.commands import hello
import warhammer_bot
import logging as log

import logging


#log.basicConfig(level=log.DEBUG)
log = logging.getLogger()
log.setLevel("DEBUG")
def send_message(WEBHOOK_ID, WEBHOOK_TOKEN, payload):
    headers = {'content-type': 'application/json'}
    url = f'https://discord.com/api/v10/webhooks/{WEBHOOK_ID}/{WEBHOOK_TOKEN}/messages/@original'
    body = {"type": 1, "content": payload}
    log.info(f"Sending message to discord")
    log.debug(f"Message details, URL: {url}, body: {payload}, Headers: {headers}")
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
        command_name = body['data']['name']
        WEBHOOK_ID = body['application_id']
        WEBHOOK_TOKEN = body['token']

        command = getattr(warhammer_bot, command_name)
        log.info(f"Handling command:{command_name}: {command}")
        payload = command()
        log.debug(f"webhook_id: {WEBHOOK_ID} webhook_token: {WEBHOOK_TOKEN[1:10]} Payload: {payload}")
        response = send_message(WEBHOOK_ID, WEBHOOK_TOKEN, payload)
        log.info(f"Response from discord: {response.status_code} {response.reason} {response.text}")
    except KeyError:
        log.error("Missing command or webhook_id or webhook_token")


