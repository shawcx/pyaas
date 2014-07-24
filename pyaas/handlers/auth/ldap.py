
import logging

import pyaas

import tornado.web

try:
    import ldap
except ImportError:
    raise pyaas.error('Missing LDAP module')


class Login(tornado.web.RequestHandler):
    def get(self):
        next = self.get_argument('next', '/')
        self.render('login.html', next=next)

    def post(self):
        username = self.get_argument('username', '')
        username = tornado.escape.xhtml_escape(username)
        password = self.get_argument('passwd', '')

        ldap_dn  = pyaas.config.get('ldap', 'dn')
        ldap_uri = pyaas.config.get('ldap', 'uri')

        try:
            dn = ldap_dn.format(username)
            ldap_server = ldap.initialize(ldap_uri)
            ldap_server.bind_s(dn, password)
            ldap_server.unbind()

            self.set_secure_cookie('uid', username)

        except ldap.INVALID_CREDENTIALS:
            # do nothing, secure cookie will not be set
            pass

        except ldap.SERVER_DOWN:
            logging.warn('Could not connect to LDAP server')
            self.set_secure_cookie('uid', username)

        self.redirect(self.get_argument('next', '/'))
