# coding: utf-8
from gomoku.constants import GameState
from gomoku.game.game import Game
from gomoku.game.users import User, logger
from gomoku.game.exceptions import AuthenticationError


class Manager:

    """Manages users and their actions"""

    def __init__(self):
        self.users = {}
        self.games = {}

    def connect(self, socket):
        user = User(socket=socket)
        self.users[socket] = user
        self.update_state()
        return user

    def disconnect(self, socket):
        try:
            user = self.users.pop(socket)
        except KeyError:
            logger.error('Attempted disconnect unregistered socket')
        else:
            game = user.game
            if game:
                game.leave(user)
                if game.state == GameState.EMPTY:
                    del self.games[game.id]
            user._socket = None
            self.update_state()

    def broadcast(self, data):
        for socket in self.users.keys():
            socket.send('BROADCAST', data)

    def update_state(self):
        self.broadcast({
            'users': [user.to_json() for user in self.users.values()],
            'games': [game.to_json() for game in self.games.values()],
        })

    def authenticate(self, name):
        name = name.strip() if name else name
        if not name:
            raise AuthenticationError('Name should not be empty')
        names = (user.name for user in self.users.values()
                 if user.is_authenticated)
        if name in names:
            raise AuthenticationError(
                'Name "{0}" is already taken'.format(name))
        return name

    def create_game(self, user, side):
        assert side in {'white', 'black'}
        game = Game()
        self.games[game.id] = game
        game.join(user, side)
        self.update_state()
        return game
