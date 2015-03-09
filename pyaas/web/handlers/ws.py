
import tornado.web
import tornado.websocket


class Broadcast(tornado.websocket.WebSocketHandler):
    def initialize(self, websockets=None):
        if websockets is None:
            self.websockets = self.application.websockets
        else:
            self.websockets = websockets

    def open(self):
        self.stream.set_nodelay(True)
        self.websockets.add(self)

    def on_message(self, msg):
        if msg == 'ping':
            return

        for ws in self.websockets:
            if ws is self:
                continue
            ws.write_message(msg)

    def on_close(self):
        try:
            self.websockets.remove(self)
        except KeyError:
            pass


class Protected(Broadcast):
    def open(self):
        if not self.get_secure_cookie('uid'):
            raise tornado.web.HTTPError(403)

        Broadcast.open(self)
