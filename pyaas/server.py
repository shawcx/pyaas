
import os
import socket
import logging

try:
    import configparser
except ImportError:
    import ConfigParser as configparser

import pyaas
import pyaas.handlers

import tornado.web
import tornado.ioloop

pyaas.ioloop = tornado.ioloop.IOLoop.instance()


class Application(tornado.web.Application):
    def __init__(self, section='server'):
        self.websockets = set()

        # get the interface and port to listen on
        self.addr = pyaas.args.address or pyaas.config.get(section, 'address')
        self.port = pyaas.args.port or pyaas.config.getint(section, 'port')

        # load the cookie secret used to encrypt cookies
        cookie_path = os.path.join(pyaas.paths.etc, 'cookie.secret')

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
            static_path   = pyaas.paths.static,
            template_path = pyaas.paths.templates,
            cookie_secret = cookie_secret,
            debug         = False
        )

        # useful during development
        if pyaas.args.debug:
            self.settings['debug'] = True

        pyaas.module.Auth().load(self)


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


