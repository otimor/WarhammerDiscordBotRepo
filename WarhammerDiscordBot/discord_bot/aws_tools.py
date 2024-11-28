import boto3
import json
import asyncio
import logging

log = logging.getLogger()
log.setLevel("DEBUG")
async def send_sns_message(**params):
    log.debug(f"creating sns client")
    sns = boto3.client('sns', api_version='2010-03-31')
    log.debug(f"Sending SNS message: {params}")
    await sns.publish(**params)


def get_sns_topic_arn(parameter_name=None):
    client = boto3.client('sns')
    response = client.list_topics(NextToken='string')
    if parameter_name is None:
        return response['Topics'][0]['TopicArn']
    for topic in response['Topics']:
        if topic['TopicArn'].endswith(parameter_name):
            return topic['TopicArn']
    return None

def get_secret(secret_name='WH_DISCORD_BOT_PUBLIC_KEY'):
    #TODO: write function to get the public key from AWS Secrets
    PUBLIC_KEY = '8327fc9706afcfc96f72c1c0010b13e6af4f6d1c3b61dfd48d867270501525ca'
    #
    #client = boto3.client('secretsmanager')
    #response = client.get_secret_value(SecretId=secret_name)
    #secret = json.loads(response['SecretString'])
    #return secret
    return PUBLIC_KEY
