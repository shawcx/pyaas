
import os
import socket
import logging

try:
    import configparser
except ImportError:
    import ConfigParser as configparser

import pyaas

import tornado.web
import tornado.ioloop

pyaas.ioloop = tornado.ioloop.IOLoop.instance()

from . import handlers


class Application(tornado.web.Application):
    def __init__(self, section='server'):
        # get the interface and port to listen on
        self.addr = pyaas.args.address or pyaas.config.get(section, 'address')
        self.port = pyaas.args.port or pyaas.config.getint(section, 'port')

        # load the cookie secret used to encrypt cookies
        cookie_path = os.path.join(pyaas.prefix, 'etc', pyaas.namespace, 'cookie.secret')

        if pyaas.args.newcookie:
            cookie_secret = pyaas.util.generateCookieSecret(cookie_path)
        else:
            try:
                with open(cookie_path, 'rb') as fp:
                    cookie_secret = fp.read(44)
            except IOError:
                cookie_secret = pyaas.util.generateCookieSecret(cookie_path)

        # URI patterns
        if not hasattr(self, 'ssl_options'):
            self.ssl_options = None

        # URI patterns
        if not hasattr(self, 'patterns'):
            self.patterns = []

        # Tornado settings
        self.settings = dict(
            static_path   = os.path.join(pyaas.prefix, 'share', pyaas.namespace, 'static'),
            template_path = os.path.join(pyaas.prefix, 'share', pyaas.namespace, 'templates'),
            cookie_secret = cookie_secret,
            debug         = False
        )

        # useful during development
        if pyaas.args.debug:
            self.settings['debug'] = True

        # get the auth mechanism if any
        try:
            auth = pyaas.config.get(section, 'auth')
        except:
            auth = None

        if auth:
            logging.debug('Enabling authentication: %s', auth)

            # all auth mechanisms need to be in this path
            path = 'pyaas.handlers.auth.' + auth
            try:
                module = __import__(path)
            except ImportError:
                raise pyaas.error('Unknown auth method: %s', auth)

            # drill done to the actual module
            for name in path.split('.')[1:]:
                module = getattr(module, name)

            try:
                Initialize = getattr(module, 'Initialize')
                logging.debug('Initializing authentication: %s', auth)
                Initialize(**dict(pyaas.config.items(auth, True)))
            except AttributeError:
                # no intialization needed
                pass
            except configparser.NoSectionError:
                raise pyaas.error('Missing configurationf for %s', auth)

            # get the Login class from the module
            try:
                Login = getattr(module, 'Login')
            except AttributeError:
                raise pyaas.error('Auth module is missing Login class')

            # extend the patterns and settings accordingly
            self.patterns.extend([
                ( r'/login',  Login                      ),
                ( r'/logout', pyaas.handlers.auth.Logout ),
                ])

            self.settings['login_url'] = '/login'

    def Listen(self):
        # initialize here so patterns and settings can be extended by plugins
        tornado.web.Application.__init__(self, self.patterns, **self.settings)

        try:
            self.listen(self.port, self.addr, xheaders=True, ssl_options=self.ssl_options)
        except socket.gaierror as e:
            if 8 == e.errno:
                raise pyaas.error('Invalid address specified "%s"' % self.addr)
            raise pyaas.error('Could not listen: %s' % e)
        except socket.error as e:
            raise pyaas.error('Could not listen: %s' % e)

        logging.info('Listening on %s:%d', self.addr, self.port)

        pyaas.ioloop.start()

    def Stop(self):
        pyaas.ioloop.stop()
