
import os
import base64
import inspect

import pyaas

def generateCookieSecret(path):
    secret = base64.b64encode(os.urandom(32))
    with open(path, 'w') as fp:
        fp.write(secret)
    return secret

# TODO: add functionality to manage basic authentication

def setroot(newroot=None):
    if not newroot:
        # inspect who called this function
        frames = inspect.getouterframes(inspect.currentframe())
        # get the caller frame
        frame = frames[1]
        # get the filename of the caller
        newroot = os.path.abspath(frame[1])
        # get the directory name of the file
        newroot = os.path.dirname(newroot)

    pyaas.root = os.path.abspath(newroot)
