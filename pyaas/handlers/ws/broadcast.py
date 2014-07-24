
import socket

import tornado.web
import tornado.websocket


class Broadcast(tornado.websocket.WebSocketHandler):
    def initialize(self, sockets):
        self.sockets = sockets

    def open(self):
        self.stream.socket.setsockopt(socket.SOL_TCP, socket.TCP_NODELAY, 1)
        self.sockets.add(self)

    def on_message(self, msg):
        if msg == 'ping':
            return

        for ws in self.sockets:
            if ws is self:
                continue
            ws.write_message(msg)

    def on_close(self):
        try:
            self.sockets.remove(self)
        except KeyError:
            pass


class Protected(Broadcast):
    def open(self):
        if not self.get_secure_cookie('uid'):
            raise tornado.web.HTTPError(403)

        Broadcast.open(self)
