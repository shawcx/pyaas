
import tornado.web


class Base(tornado.web.RequestHandler):
    def set_default_headers(self):
        self.set_header('Server', 'Pyaas Web Service')

    def get_current_user(self):
        uid = self.get_secure_cookie('uid')
        if uid is None:
            self.clear_cookie('uid')
        return uid


from .index import *
from .      import ws
