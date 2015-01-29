__author__ = 'mriley'

from .decorator import *


class CacheModule(pyaas.module.PyaasModule):
    PKG_PATH = 'pyaas.cache'


#class Cache(PyaasModule):
#    """
#    Pyaas cache module
#    """
#    def __init__(self):
#        super(Cache, self).__init__('cache', 'pyaas.cache', 'Cache')
#
#    def load(self, application=None):
#        pyaas.cache = self.getInstance()
#        if pyaas.cache:
#            logging.debug('Enabled cache: %s', self.implName)
#
