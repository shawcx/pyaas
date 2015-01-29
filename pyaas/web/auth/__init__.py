
# login methods are dynamically imported if auth is enabled

import logging

from .logout import Logout

import pyaas

class AuthModule(pyaas.module.PyaasModule):
    PKG_PATH = 'pyaas.web.auth'

    @classmethod
    def load(cls):
        if not pyaas.config.has_option('modules', 'auth'):
            return

        instances = pyaas.config.get('modules', 'auth')
        instances = [instance.strip() for instance in instances.split(',')]
        for instance in instances:
            logging.info('Loading authentication: %s', instance)

            if not pyaas.config.has_section(instance):
                logging.warn('No configuration for authentication: %s', instance)
                continue

            params = dict(pyaas.config.items(instance))

            url = params.pop('login', '/login')

            authClass = cls.loadModule(instance)
            authClass.URL = url

        return


#class Auth(PyaasModule):
#    """
#    Pyaas auth module
#    """
#    def __init__(self):
#        super(Auth, self).__init__('auth', 'pyaas.web.auth', 'Login')
#
#    def load(self, application=None):
#        login = self.getClass()
#        if login:
#            # extend the patterns and settings accordingly
#            application.patterns.extend([
#                ( r'/login',  login                 ),
#                ( r'/logout', pyaas.web.auth.Logout ),
#                ])
#
#            application.settings['login_url'] = '/login'
#
#            logging.debug('Enabled authentication: %s', self.implName)
