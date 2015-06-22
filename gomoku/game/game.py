# coding: utf-8
from datetime import datetime
import logging
from uuid import uuid4

from gomoku.constants import GameState
from gomoku.game.board import Board
from gomoku.game.exceptions import IllegalMoveError


BOARD_SIZE = 15

logger = logging.getLogger(__name__)


class Game:

    def __init__(self):
        self.id = str(uuid4())
        self.board = Board(size=BOARD_SIZE)
        self.created = datetime.now()
        self.started = None
        self.winner = None
        self.moves = 0

        self.players = {
            'black': None,
            'white': None,
        }

    @property
    def state(self):
        players_count = len(list(filter(None, self.players.values())))
        if players_count == 0:
            return GameState.EMPTY
        if self.winner:
            return GameState.FINISHED
        if players_count == 1:
            return GameState.WAITING
        return GameState.IN_PROGRESS

    @property
    def turn(self):
        return 'black' if self.moves % 2 == 0 else 'white'

    def join(self, user, side):
        assert side in {'black', 'white'}

        players = self.players
        if players[side] is not None:
            logger.error('Attempted to join, but side is already taken')
            return

        other_side = 'black' if side == 'white' else 'white'
        if user.game and user.game is not self:
            user.game.leave(user)

        user.game = self
        user.side = side

        players[side] = user
        if players[other_side] is user:
            players[other_side] = None

        if players['black'] and players['white']:
            self.started = datetime.now()

        self.notify_players()

    def leave(self, user):
        for side, player in self.players.items():
            if player is user:
                self.players[side] = None
                user.game = None

                if self.state == GameState.IN_PROGRESS:
                    self.board = Board(size=BOARD_SIZE)
                    self.started = None
                    self.moves = None

                player.update_state()
                self.notify_players()
                return

    def make_move(self, x, y, side):
        assert side in {'black', 'white'}

        if self.state != GameState.IN_PROGRESS:
            raise IllegalMoveError('Game is not in progress')

        if self.turn != side:
            raise IllegalMoveError('This is not your turn')

        try:
            if self.board.get(x, y):
                raise IllegalMoveError('This cell is taken')
        except IndexError:
            raise IllegalMoveError('Bad coordinates')

        self.board.set(x, y, 1 if side == 'black' else 2)
        self.moves += 1

        if self.board.is_winning(x, y):
            self.winner = side

        self.notify_players()

    def to_json(self):
        black = self.players['black']
        white = self.players['white']
        started = self.started
        return {
            'id': self.id,
            'state': int(self.state),
            'turn': self.turn,
            'started': str(started) if started else None,
            'winner': self.winner,
            'black': black.to_json(short=True) if black else None,
            'white': white.to_json(short=True) if white else None,
            'board': self.board.to_json() if started else None,
        }

    def notify_players(self):
        for player in self.players.values():
            if player:
                player.update_state()
