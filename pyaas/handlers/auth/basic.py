
import os
import hashlib
import base64

import pyaas

import tornado.web

# TODO: this is opening the file and scanning it for every login, which is fine
#       for small projects with a limited number of users.  Long term this
#       this should be updated to support faster lookups

# Passwords can be managed with Apache's htpasswd program

class Login(tornado.web.RequestHandler):
    def get(self):
        self.render('login.html')

    def post(self):
        username = self.get_argument('username', 'admin')
        password = self.get_argument('password', '')
        password = '{SHA}' + base64.b64encode(hashlib.sha1(password).digest()) + '\n'

        path = os.path.join(pyaas.prefix, pyaas.config.get('basic', 'path'))
        fp = open(path, 'r')
        for line in fp:
            if not line:
                continue
            entry,hash = line.split(':', 1)

            if entry != username:
                continue

            if hash != password:
                break
                #raise tornado.web.HTTPError(403)

            self.set_secure_cookie('uid', username)
            break

        self.redirect(self.get_argument('next', '/'))
