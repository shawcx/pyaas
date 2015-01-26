
import sys
import os
import argparse
import collections
import inspect
import logging

try:
    import configparser
except ImportError:
    import ConfigParser as configparser

import pyaas

pyaas.argparser = argparse.ArgumentParser()

pyaas.argparser.add_argument('--address', '-a',
    help = 'Interface to bind to')

pyaas.argparser.add_argument('--port', '-p',
    type=int,
    help='Port to bind to')

pyaas.argparser.add_argument('--newcookie',
    action='store_true',
    help='Generate a new cookie')

pyaas.argparser.add_argument('--ini', '-i',
    help='Specify additional ini file')

pyaas.argparser.add_argument('--debug', '-d',
    action='store_true',
    help='Print verbose debugging information')

logging.basicConfig(
    format  = '%(asctime)s %(levelname)-8s %(message)s',
    datefmt = '%Y-%m-%d %H:%M:%S',
    level   = logging.INFO
)


def load(program=None):
    if program is None:
        program = os.path.basename(sys.argv[0])

        if program.endswith('.py'):
            program = program.rsplit('.', 1)[0]

    pyaas.args = pyaas.argparser.parse_args()

    pyaas.config = configparser.SafeConfigParser(dict_type=collections.OrderedDict)
    pyaas.config.optionxform = str

    ini_files = [
        os.path.join(pyaas.prefix, 'etc', pyaas.namespace, program + '.ini'),
        os.path.join(pyaas.prefix, 'etc', pyaas.namespace, program + '.ini.local')
    ]

    if pyaas.args.ini:
        ini_files.append(pyaas.args.ini)

    try:
        ok = pyaas.config.read(ini_files)
    except configparser.ParsingError as e:
        raise pyaas.error('Unable to parse file: %s', e)

    if not ok:
        raise pyaas.error('Unable to read config file(s): %s', ini_files)

    # setup file log
    root = logging.getLogger()
    fh = logging.FileHandler(os.path.join(pyaas.paths.var, program + '.log'))
    fh.setLevel(logging.INFO)

    if pyaas.args.debug:
        root.setLevel(logging.DEBUG)
        fh.setLevel(logging.DEBUG)

    formatter = logging.Formatter(
        fmt = '%(asctime)s %(levelname)-8s %(message)s',
        datefmt = '%Y-%m-%d %H:%M:%S',
        )

    fh.setFormatter(formatter)

    # add the handlers to the logger
    root.addHandler(fh)


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
        logging.info('Setting prefix to "%s"', pyaas.prefix)


def setNameSpace(namespace=None):
    if namespace is None:
        # inspect who called this function
        frames = inspect.getouterframes(inspect.currentframe())
        # get the caller frame
        frame = frames[-1]
        namespace = os.path.basename(frame[1]).split('.')[0]

    if namespace != pyaas.namespace:
        pyaas.namespace = namespace
        logging.info('Setting namespace to "%s"', pyaas.namespace)


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

    Paths = collections.namedtuple('Paths', ['etc', 'share', 'var'])
    pyaas.paths = Paths(
        etc   = os.path.join(pyaas.prefix, 'etc',   pyaas.namespace),
        share = os.path.join(pyaas.prefix, 'share', pyaas.namespace),
        var   = os.path.join(pyaas.prefix, 'var',   pyaas.namespace),
        )

    # Init settings
    pyaas.settings.load(settings)

    # Init global modules
    pyaas.module.Cache().load()
    pyaas.module.Storage().load()
