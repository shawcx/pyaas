
import tornado.web

from pyaas.web.handlers import Base


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
