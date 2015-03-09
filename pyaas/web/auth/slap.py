
import time
import logging

import pyaas

import tornado.web

try:
    import ldap
except ImportError:
    raise pyaas.error('Missing LDAP module')


class Slap(tornado.web.RequestHandler):
    def get(self):
        next = self.get_argument('next', '/')
        self.render('login.html', next=next)

    def post(self):
        username = self.get_argument('username', '')
        username = tornado.escape.xhtml_escape(username)
        password = self.get_argument('password', '')

        ldap_dn  = pyaas.config.get('slap', 'dn')
        ldap_uri = pyaas.config.get('slap', 'uri')

        try:
            dn = ldap_dn.format(username)
            ldap_server = ldap.initialize(ldap_uri)
            ldap_server.bind_s(dn, password)

            record = ldap_server.search_s(dn, ldap.SCOPE_BASE, '(objectClass=*)')[0][1]
            if 'shadowMax' in record and 'shadowLastChange' in record:
                try:
                    shadowMax = int(record['shadowMax'][0])
                    lastChange = int(record['shadowLastChange'][0])
                except ValueError:
                    # skip expiration check on exception
                    shadowMax = time.time() / 86400

                if ((time.time() / 86400) - shadowMax) > lastChange:
                    try:
                        expired = pyaas.config.get('slap', 'expired')
                        self.redirect(expired)
                        return
                    except:
                        pass

            self.set_secure_cookie('uid', username)
            ldap_server.unbind()

        except ldap.NO_SUCH_OBJECT:
            logging.warn('Could not find record for user: %s', username)

        except ldap.INVALID_CREDENTIALS:
            logging.warn('Invalid credentials for user: %s', username)

        except ldap.SERVER_DOWN:
            logging.warn('Could not connect to LDAP server: %s', ldap_uri)

        self.redirect(self.get_argument('next', '/'))
