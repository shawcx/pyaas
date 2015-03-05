
import os
import socket
import logging

try:
    import configparser
except ImportError:
    import ConfigParser as configparser

import pyaas
import pyaas.web.handlers

import tornado.web
import tornado.ioloop

pyaas.ioloop = tornado.ioloop.IOLoop.instance()


class Application(tornado.web.Application):
    def __init__(self, section='server'):
        self.websockets = set()

        section = pyaas.args.name or section

        if not pyaas.config.has_section(section):
            raise pyaas.error('Invalid instance name: %s', section)

        # get the interface and port to listen on
        self.addr = pyaas.args.address or pyaas.config.get(section, 'address')
        self.port = pyaas.args.port or pyaas.config.getint(section, 'port')

        # load the cookie secret used to encrypt cookies
        cookie_path = pyaas.paths('etc', 'cookie.secret')

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
            static_path   = pyaas.paths('share', 'static'),
            template_path = pyaas.paths('share', 'templates'),
            cookie_secret = cookie_secret,
            debug         = False
        )

        # useful during development
        if pyaas.args.debug:
            self.settings['debug'] = True

            self.patterns.append(
                ( r'/src/(.*)', pyaas.web.handlers.Source ),
                )

        authModules = pyaas.module.PyaasModule.CLASSES.get('AuthModule', None)
        if authModules:
            for (name,authModule) in authModules.items():
                # extend the patterns and settings accordingly
                self.patterns.extend([
                    ( authModule.URL, authModule ),
                    ( r'/logout', pyaas.web.auth.Logout ),
                    ])

            logging.debug('Setting default login URL to: %s', authModule.URL)
            self.settings['login_url'] = authModule.URL


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

    def Broadcast(self, msg):
        'Broadcast a message to all connected sockets'

        for client in self.websockets:
            client.write_message(msg)

    def Stop(self):
        pyaas.ioloop.stop()


