
import tornado.auth

#
# Google authentication
#

_domains = []


def Initialize(domains):
    _domains.extend([d for d in domains.split(' ') if d])


class Login(tornado.web.RequestHandler, tornado.auth.GoogleMixin):
    @tornado.web.asynchronous
    def get(self):
        if self.get_argument('openid.mode', None):
            self.get_authenticated_user(self.async_callback(self._on_auth))
            return
        self.authenticate_redirect()

    def _on_auth(self, user):
        if not user:
            raise tornado.web.HTTPError(500, 'Google authentication failed')

        try:
            name, domain = user['email'].split('@', 1)
        except:
            raise tornado.web.HTTPError(500, 'Google authentication failed')

        if _domains and domain not in _domains:
            raise tornado.web.HTTPError(404, 'Invalid domain')

        self.set_secure_cookie('uid', name)

        self.redirect(self.get_argument('next', '/'))

    def write_error(self, status_code, **kwargs):
        #''.join("<strong>%s</strong>: %s<br/>" % (k, self.request.__dict__[k]) for k in self.request.__dict__.keys())
        #if 'exc_info' not in kwargs:
        #    return

        e = kwargs['exc_info'][1]

        self.set_header('Content-Type', 'text/html')
        self.finish('''
            <html>
                <head><title>%s</title></head>
                <body><p>%s</p></body>
            </html>''' % (status_code, e.log_message))
