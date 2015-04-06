
import sys
import os
import argparse
import collections
import logging
import time

try:
    import configparser
except ImportError:
    import ConfigParser as configparser

import pyaas

pyaas.argparser = argparse.ArgumentParser()

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



def load(settings=None, namespace=None, prefix=None):
    """
    Call this guy to init pyaas stuffs
    :param settings: Alternative name of ini file to load
    :param namespace: Namespace is used to derive paths, pass '' for an empty namespace
    :param prefix: The root path of the app
    :return: None
    """

    parent = pyaas.util.getParent()
    script_name = os.path.basename(parent)
    script_name = script_name.rsplit('.', 1)[0]

    if prefix is None:
        # get the filename of the caller
        # get the directory name of the file
        prefix = os.path.dirname(parent)

        if prefix.endswith(os.path.sep + 'bin'):
            prefix = os.path.join(prefix, '..')
            prefix = os.path.abspath(prefix)

    prefix = os.path.abspath(prefix)
    if pyaas.prefix != prefix:
        pyaas.prefix = prefix
        logging.debug('Setting prefix to "%s"', pyaas.prefix)

    if namespace is None:
        namespace = script_name

    if namespace != pyaas.namespace:
        pyaas.namespace = namespace
        logging.debug('Setting namespace to "%s"', pyaas.namespace)

    # if settings is not passed in use the supplied or derived namespace
    settings = settings or namespace

    pyaas.args = pyaas.argparser.parse_args()

    pyaas.config = configparser.SafeConfigParser(dict_type=collections.OrderedDict)
    pyaas.config.optionxform = str

    ini_files = [
        pyaas.paths('etc', settings + '.ini'),
        pyaas.paths('etc', settings + '.ini.local')
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
    file_name = '%s_%s.log' % (script_name, time.strftime('%Y%m%d_%H%M%S'))

    # hack back in single log file option without breaking existing code
    if pyaas.config.has_section('logging'):
        if pyaas.config.has_option('logging', 'append'):
            append = pyaas.config.getboolean('logging', 'append')
            if append:
                file_name = script_name + '.log'

    full_path = pyaas.paths('var', file_name)
    logfile = logging.FileHandler(full_path)
    logfile.setLevel(logging.INFO)

    logfile.setFormatter(
        logging.Formatter(
            fmt = '%(asctime)s %(levelname)-8s %(message)s',
            datefmt = '%Y-%m-%d %H:%M:%S',
            )
        )

    # add the handlers to the logger
    root = logging.getLogger()
    root.addHandler(logfile)

    if pyaas.args.debug:
        root.setLevel(logging.DEBUG)
        logfile.setLevel(logging.DEBUG)

    # call this here if there is no daemon option
    if not hasattr(pyaas.args, 'daemon'):
        pyaas.module.load()

    return
