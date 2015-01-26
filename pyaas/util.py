
import os
import base64
import logging

import pyaas

def generateCookieSecret(path):
    secret = base64.b64encode(os.urandom(32))
    with open(path, 'w') as fp:
        fp.write(secret)
    return secret
