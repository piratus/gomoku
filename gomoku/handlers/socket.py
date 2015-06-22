# coding: utf-8
import logging

from funcy import select_values
from tornado.escape import json_decode
from tornado.websocket import (
    WebSocketHandler,
    WebSocketClosedError,
)

from gomoku.constants import (
    MESSAGE_GAME_CREATE,
    MESSAGE_GAME_JOIN,
    MESSAGE_USER_LOGIN,
    MESSAGE_GAME_MOVE,
    MESSAGE_GAME_LEAVE,
)
from gomoku.handlers.messages import (
    handle_game_create,
    handle_user_login,
    handle_game_join,
    handle_game_move,
    handle_game_leave)


logger = logging.getLogger(__name__)


class SocketHandler(WebSocketHandler):

    handlers = {
        MESSAGE_USER_LOGIN: handle_user_login,
        MESSAGE_GAME_CREATE: handle_game_create,
        MESSAGE_GAME_JOIN: handle_game_join,
        MESSAGE_GAME_MOVE: handle_game_move,
        MESSAGE_GAME_LEAVE: handle_game_leave,
    }

    """
    Game WebSocket handler implementation.
    """

    user = None
    manager = None

    def initialize(self, manager=None):
        self.manager = manager
        self.handlers = SocketHandler.handlers

    def open(self):
        logger.info('Client connected')
        self.user = self.manager.connect(self)

    def on_close(self):
        logger.info('Connection closed')
        self.manager.disconnect(self)

    def on_message(self, data):
        logger.info('Got message: %r', data)

        message_name, body = parse_message(data)

        if message_name in self.handlers:
            try:
                self.handlers[message_name](self, body)
            except Exception:
                logger.exception('Unhandled exception')
        else:
            logger.error('No handler for message "%s"', message_name)

    def send(self, message_name, body=None):
        """Encode and send a message to client"""
        try:
            self.write_message(select_values(None, {
                'MESSAGE': message_name,
                'BODY': body,
            }))
        except WebSocketClosedError:
            logger.error('Error sending message', exc_info=True)

    def get_compression_options(self):
        """Enables compression"""
        return {}


def parse_message(data):
    try:
        message = json_decode(data)
        message_name = message['MESSAGE']
    except ValueError:
        logger.exception('Failed to parse incoming data: %s', data)
        return None, None
    except KeyError:
        logger.error('Bad message format: %s', data)
        return None, None

    return message_name, message.get('BODY')
