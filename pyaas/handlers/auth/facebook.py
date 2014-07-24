
import datetime

import pyaas

import tornado.auth

#
# Facebook Authentication
#

FBURL = '%s://%s/login/facebook?next=%s'


class Login(tornado.web.RequestHandler, tornado.auth.FacebookGraphMixin):
    @tornado.web.asynchronous
    def get(self):
        redir = tornado.escape.url_escape(self.get_argument('next', '/'))
        my_url = FBURL % (self.request.protocol, self.request.host, redir)

        code = self.get_argument('code', None)

        if code:
            self.get_authenticated_user(
                redirect_uri  = my_url,
                client_id     = pyaas.config.get('facebook', 'api_key'),
                client_secret = pyaas.config.get('facebook', 'secret'),
                code          = code,
                callback      = self.async_callback(self._on_auth)
            )
        else:
            self.authorize_redirect(
                redirect_uri = my_url,
                client_id    = pyaas.config.get('facebook', 'api_key'),
                extra_params = {'scope': 'email'}
            )

    def _on_auth(self, fbuser):
        if not fbuser:
            raise tornado.web.HTTPError(500, 'Facebook authentication failed')

        profile = pyaas.db.FindProfile('fbid', fbuser['id'])
        if not profile:
            self.facebook_request(
                '/me',
                access_token = fbuser['access_token'],
                callback     = self.async_callback(self._on_me)
            )
        else:
            self.set_secure_cookie('uid', str(profile['uid']))
            self.redirect(self.get_argument('next', '/'))

    def _on_me(self, fbuser):
        profile = pyaas.db.FindProfile('email', fbuser['email'])
        if not profile:
            profile = dict(
                email      = fbuser['email'],
                display    = fbuser['name'],
                fbid       = fbuser['id'],
                firstLogin = datetime.datetime.now()
            )

            uid = pyaas.db.SaveProfile(profile)
            self.set_secure_cookie('uid', str(uid))

        else:
            self.set_secure_cookie('uid', str(profile['uid']))
            # TODO: update facebook id

        self.redirect(self.get_argument('next', '/'))
