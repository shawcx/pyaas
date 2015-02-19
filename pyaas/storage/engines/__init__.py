
import logging

import pyaas

class StorageModule(pyaas.module.PyaasModule):
    PKG_PATH = 'pyaas.storage.engines'

    @classmethod
    def load(cls):
        if not pyaas.config.has_option('modules', 'storage'):
            return

        instances = pyaas.config.get('modules', 'storage')
        instances = [instance.strip() for instance in instances.split(',')]
        for instance in instances:
            logging.info('Loading storage instance: %s', instance)

            if not pyaas.config.has_section(instance):
                logging.warn('No configuration for instance: %s', instance)
                continue

            if not pyaas.config.has_option(instance, 'engine'):
                logging.warn('No engine specified for instance: %s', instance)
                continue

            params = dict(pyaas.config.items(instance))

            engine = params.pop('engine')

            engineClass = cls.loadModule(engine)

            # convert user supplied engine name into a single value
            section = engine.split('.')[-1]

            if pyaas.config.has_section(section):
                options = dict(pyaas.config.items(section))
            else:
                options = {}

            options.update(params)

            isCritical = options.pop('critical', 'true')
            try:
                pyaas.storage.databases[instance] = engineClass(**options)
                pyaas.storage.databases[instance].Initialize()
            except pyaas.error as e:
                if isCritical.lower() in ['false', 'f' 'no', 'n', '0']:
                    logging.warn('Unable to instantiate engine: %s:%s', engine, instance)
                    logging.debug('%s', e)
                else:
                    raise

        return
