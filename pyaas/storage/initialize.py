
import logging

import pyaas


def initialize(engine=None, section=None):
    if not engine:
        engine = pyaas.args.db or pyaas.config.get('storage', 'engine')

    path = 'pyaas.storage.engines.' + engine

    try:
        mod = __import__(path)
    except ImportError:
        raise pyaas.error('Unknown storage engine: %s', engine)

    for sub in path.split('.')[1:]:
        mod = getattr(mod, sub)

    try:
        dbcls = getattr(mod, 'Database')
    except AttributeError:
        raise pyaas.error('Bad storage engine: %s', engine)

    logging.info('Storage engine: %s', engine)

    if not section:
        section = engine

    options = {}
    if pyaas.config.has_section(section):
        options = dict(pyaas.config.items(section))

    logging.debug('Options: %s', options)

    pyaas.db = dbcls(**options)

    if pyaas.args.initdb:
        pyaas.db.Initialize()

    return pyaas.db
