#Authorizer for the discord bot

from nacl.signing import VerifyKey
from nacl.exceptions import BadSignatureError
import logging

#log.basicConfig(level=log.DEBUG)
log = logging.getLogger()
#log.setLevel("DEBUG")

def check_auth(publickey, signature, timestamp, body):
    log.debug(f'Verifying {signature} with timestamp {timestamp} body: {body}')
    verify_key = VerifyKey(bytes.fromhex(publickey))
    message = timestamp + body
    try:
        verify_key.verify(message.encode(), signature=bytes.fromhex(signature))
    except BadSignatureError:
        log.error("validate: Message validation failed!")
        return False, 'invalid request signature'
    log.debug("validate: Message validated, succesfully")
    return True, 'valid request signature'


class DiscordBotAuthorizer:
    def __init__(self, public_key):
        self.public_key = bytes.fromhex(public_key)

    def validate(self, signature, timestamp, body):
        log.debug(f'Verifying {signature} with timestamp {timestamp} body: {body}')
        verify_key = VerifyKey(self.public_key)
        message = timestamp + body
        log.debug(f'Validating message: {message}')
        try:
            verify_key.verify(message.encode(), signature=bytes.fromhex(signature))
        except BadSignatureError:
            return False, 'invalid request signature'

        log.debug("Message validated, succesfully")
        return True, 'valid request signature'