
import sys
import os
import argparse
import collections
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
    level   = 0
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

    # TODO: log to file

    #root = logging.getLogger()
