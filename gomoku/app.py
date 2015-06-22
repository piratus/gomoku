# coding: utf-8
from tornado.web import Application as TornadoApplication
from gomoku.game.manager import Manager

from gomoku.handlers.index import IndexHandler
from gomoku.handlers.socket import SocketHandler


class Application(TornadoApplication):

    def __init__(self, **settings):

        self.users = Manager()

        super().__init__([
            (r'/', IndexHandler),
            (r'/socket', SocketHandler, dict(manager=self.users)),
        ], **settings)
