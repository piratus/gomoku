# coding: utf-8
import logging
from uuid import uuid4

from funcy import merge

from gomoku.constants import (
    MESSAGE_USER_UPDATE_STATE,
)


logger = logging.getLogger(__name__)


class User:

    def __init__(self, socket=None, name='', game=None):
        self._socket = socket
        self.id = str(uuid4())
        self._name = name
        self.game = game
        self.side = None

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value
        self.update_state()

    @property
    def is_authenticated(self):
        return bool(self._name)

    def to_json(self, short=False):
        data = {
            'id': self.id,
            'name': self._name,
        }

        return data if short else merge(data, {
            'isAuthenticated': self.is_authenticated,
            'game': self.game and self.game.to_json(),
            'side': self.side,
        })

    def update_state(self):
        if self._socket:
            self._socket.send(MESSAGE_USER_UPDATE_STATE, {
                'user': self.to_json(),
            })
