
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
            cls.loadInstance(instance)
        return

    @classmethod
    def loadInstance(cls, instance, instance_dup=None, **kwargs):
        logging.info('Loading storage instance: %s', instance)
        conf = pyaas.config

        if 'engine' in kwargs:
            engine = kwargs.pop('engine')
        elif conf.has_section(instance) and conf.has_option(instance, 'engine'):
            engine = pyaas.config.get(instance, 'engine')
        elif instance_dup is not None and conf.has_section(instance_dup) and conf.has_option(instance_dup, 'engine'):
            engine = pyaas.config.get(instance_dup, 'engine')
        else:
            logging.warn('No configuration for instance: %s', instance)
            return None

        engine_class = cls.loadModule(engine)

        # convert user supplied engine name into a single value
        engine_defaults = engine.split('.')[-1]

        # cascade settings
        options = {}
        if conf.has_section(engine_defaults):
            options.update(dict(conf.items(engine_defaults)))
        if instance_dup is not None and conf.has_section(instance_dup):
            options.update(dict(conf.items(instance_dup)))
        if conf.has_section(instance):
            options.update(dict(conf.items(instance)))
        options.update(kwargs)

        options.pop('engine')
        critical = options.pop('critical', 'true')
        try:
            opts = dict(options)
            opts['password'] = '****'
            logging.debug('Loading storage instance %s with args %s', instance, opts)
            pyaas.storage.databases[instance] = db = engine_class(**options)
            db.Initialize()
            return db
        except pyaas.error as e:
            if critical.lower() in ['false', 'f' 'no', 'n', '0']:
                logging.warn('Unable to instantiate engine: %s:%s', engine, instance)
                logging.debug('%s', e)
            else:
                raise
        return None