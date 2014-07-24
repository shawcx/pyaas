
import tornado.web


class Base(tornado.web.RequestHandler):
    def get_current_user(self):
        uid = self.get_secure_cookie('uid')
        if uid is None:
            self.clear_cookie('uid')
        return uid


class Index(Base):
    def initialize(self, template='index'):
        self.template = template + '.html'

    def get(self, template=None):
        template = template + '.html' if template else self.template
        self.render(template)


class Protected(Base):
    def initialize(self, template='index'):
        self.template = template + '.html'

    @tornado.web.authenticated
    def get(self, template=None):
        template = template + '.html' if template else self.template
        self.render(template)
