__author__ = 'mriley'

import logging
import pyaas

from .decorator import *


class CacheModule(pyaas.module.PyaasModule):
    PKG_PATH = 'pyaas.storage.cache'

    @classmethod
    def load(cls):
        if not pyaas.config.has_option('modules', 'cache'):
            return

        instances = pyaas.config.get('modules', 'cache')
        instances = [instance.strip() for instance in instances.split(',')]
        instances.reverse()
        for instance in instances:
            logging.info('Loading cache: %s', instance)

            if not pyaas.config.has_section(instance):
                params = {}
            else:
                params = dict(pyaas.config.items(instance))

            cache_class = cls.loadModule(instance)
            if pyaas.cache is None:
                pyaas.cache = cache_class(**params)
            else:
                params['next'] = pyaas.cache
                pyaas.cache = cache_class(**params)
        return
