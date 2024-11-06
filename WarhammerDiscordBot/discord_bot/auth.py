#Authorizer for the discord bot

from nacl.signing import VerifyKey
from nacl.exceptions import BadSignatureError

class DiscordBotAuthorizer:
    def __init__(self, public_key):
        self.public_key = public_key

    def validate(self, signature, timestamp, body):
        verify_key = VerifyKey(bytes.fromhex(self.public_key))

        message = timestamp + body

        try:
            verify_key.verify(message.encode(), signature=bytes.fromhex(signature))
        except BadSignatureError:
            return False, 'invalid request signature'

        return True