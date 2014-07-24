
import tornado.web


class Logout(tornado.web.RequestHandler):
    def get(self):
        self.clear_cookie('uid')
        self.redirect(self.get_argument('next', '/'))
