
import os
import base64
import inspect
import logging

import pyaas

class Paths(object):
    def __init__(self):
        self.etc = None
        self.static = None
        self.templates = None

def generateCookieSecret(path):
    secret = base64.b64encode(os.urandom(32))
    with open(path, 'w') as fp:
        fp.write(secret)
    return secret


def setPrefix(prefix=None):
    if not prefix:
        # inspect who called this function
        frames = inspect.getouterframes(inspect.currentframe())
        # get the caller frame
        frame = frames[-1]
        # get the filename of the caller
        prefix = os.path.abspath(frame[1])
        # get the directory name of the file
        prefix = os.path.dirname(prefix)

        if prefix.endswith(os.path.sep + 'bin'):
            prefix = os.path.join(prefix, '..')
            prefix = os.path.abspath(prefix)

    prefix = os.path.abspath(prefix)
    if pyaas.prefix != prefix:
        pyaas.prefix = prefix
        logging.debug('Setting prefix to "%s"', pyaas.prefix)


def setNameSpace(namespace=None):
    if namespace is None:
        # inspect who called this function
        frames = inspect.getouterframes(inspect.currentframe())
        # get the caller frame
        frame = frames[-1]
        namespace = os.path.basename(frame[1]).split('.')[0]

    if namespace != pyaas.namespace:
        pyaas.namespace = namespace
        logging.debug('Setting namespace to "%s"', pyaas.namespace)


def init(prefix='', namespace='', settings=None):
    """
    Call this guy to init pyaas stuffs
    :param prefix: The root path of the app
    :param namespace: The namespace
    :param settings: Alternative name of ini file to load
    :return: None
    """

    # Set my prefix
    setPrefix(prefix)
    # Set my namespace
    setNameSpace(namespace)

    # Set other fun things based on these
    pyaas.paths = Paths()
    pyaas.paths.etc = os.path.join(pyaas.prefix, 'etc', pyaas.namespace)
    pyaas.paths.static = os.path.join(pyaas.prefix, 'share', pyaas.namespace, 'static')
    pyaas.paths.templates = os.path.join(pyaas.prefix, 'share', pyaas.namespace, 'templates')

    # Init settings
    pyaas.settings.load(settings)

    # Init global modules
    pyaas.module.Cache().load()
    pyaas.module.Storage().load()
