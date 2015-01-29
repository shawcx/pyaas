
import logging

from .records    import *

import pyaas

#pyaas.argparser.add_argument('--db',
#    help='Select storage engine')
#
#pyaas.argparser.add_argument('--initdb',
#    action='store_true',
#    help='Initialize the database')

pyaas.databases = {}


def initialize():
    if not pyaas.config.has_option('modules', 'storage'):
        return

    def loadEngine(engine):
        # try loading a user-supplied engine first
        try:
            path = engine
            mod = __import__(path)
        except ImportError:
            # then try loading a pyaas engine next
            try:
                path = 'pyaas.storage.engines.' + engine
                mod = __import__(path)
            except ImportError:
                raise pyaas.error('Unknown storage engine: %s', engine)

        for sub in path.split('.')[1:]:
            mod = getattr(mod, sub)

        classname = sub.capitalize()

        engineClass = getattr(mod, classname, None)
        if engineClass is None:
            try:
                engineClass = getattr(mod, 'Database')
            except AttributeError:
                raise pyaas.error('Bad storage engine: %s', engine)

        return engineClass


    engines = pyaas.config.get('modules', 'storage')
    engines = [e.strip() for e in engines.split(',')]
    for engine in engines:
        logging.info('Loading storage engine: %s', engine)
        engineClass = loadEngine(engine)

        # convert user supplied engine name into a single value
        section = engine.split('.')[-1]

        options = {}
        if pyaas.config.has_section(section):
            options = dict(pyaas.config.items(section))

            instances = options.pop('instances', None)
            if instances is not None:
                for name in [i.strip() for i in instances.split(',')]:
                    instance_options = options.copy()
                    if pyaas.config.has_section(section + ':' + name):
                        instance_options.update(pyaas.config.items(section + ':' + name))

                    critical = instance_options.pop('critical', 'true')
                    try:
                        instance = engineClass(**instance_options)
                        pyaas.databases[name] = instance
                    except pyaas.error as e:
                        if critical.lower() in ['false', 'f' 'no', 'n', '0']:
                            logging.warn('Unable to instantiate engine: %s:%s', engine, name)
                            logging.debug('%s', e)
                        else:
                            raise
            else:
                raise pyaas.error('TODO: default instance name')
        else:
            raise pyaas.error('TODO: default options')

    return


