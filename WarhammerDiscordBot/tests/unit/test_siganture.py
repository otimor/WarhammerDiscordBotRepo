import pytest
from nacl.signing import SigningKey
from nacl.encoding import HexEncoder
import json
from datetime import datetime

PUBLIC_KEY = '8327fc9706afcfc96f72c1c0010b13e6af4f6d1c3b61dfd48d867270501525ca'
test_url = 'https://r35tcp1wl0.execute-api.us-west-2.amazonaws.com/Prod/WarhammerDiscordBot'
def generate_signature(message=None, timestamp=None):# Example message and timestamp
    if message is None:
        message = '{"type": "1", "data": {"name": "hello"}}'
    if timestamp is None:
        timestamp = datetime.utcnow().isoformat() + 'Z'

    # Combine timestamp and message
    combined_message = timestamp + message

    # Create a VerifyKey object
    signing_key = SigningKey(PUBLIC_KEY, encoder=HexEncoder)

    # Calculate the signature
    signature = signing_key.sign(combined_message.encode()).signature

    # Print the signature in hexadecimal format
    print(signature.hex())
    #print headers
    test_curl_command = f'curl -vv -X POST "{test_url}" -d "{message}" -H "Content-Type: application/json" -H "x-signature-ed25519: {signature.hex()}" -H "x-signature-timestamp: {timestamp}"'
    print(f'curl command: {test_curl_command}')

if __name__ == '__main__':
    generate_signature() # Call the function
    #pytest.main(['-v', __file__]) # Run the tests