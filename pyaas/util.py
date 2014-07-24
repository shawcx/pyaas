
import os
import base64
import inspect
import logging

import pyaas


def generateCookieSecret(path):
    secret = base64.b64encode(os.urandom(32))
    with open(path, 'w') as fp:
        fp.write(secret)
    return secret

# TODO: add functionality to manage basic authentication


def setPrefix(prefix=None):
    if not prefix:
        # inspect who called this function
        frames = inspect.getouterframes(inspect.currentframe())
        # get the caller frame
        frame = frames[1]
        # get the filename of the caller
        prefix = os.path.abspath(frame[1])
        # get the directory name of the file
        prefix = os.path.dirname(prefix)

        if prefix.endswith(os.path.sep + 'bin'):
            prefix = os.path.join(prefix, '..')
            prefix = os.path.abspath(prefix)

    pyaas.prefix = os.path.abspath(prefix)
    logging.debug('Setting prefix to "%s"', pyaas.prefix)


def setNameSpace(namespace=None):
    if namespace is None:
        # inspect who called this function
        frames = inspect.getouterframes(inspect.currentframe())
        # get the caller frame
        frame = frames[1]
        namespace = frame[0].f_code.co_name
        logging.debug('Setting namespace to "%s"', namespace)

    pyaas.namespace = namespace
