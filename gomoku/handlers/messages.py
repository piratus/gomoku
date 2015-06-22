# coding: utf-8
from gomoku.constants import MESSAGE_USER_LOGIN_ERROR, MESSAGE_GAME_ERROR
from gomoku.game.exceptions import (
    AuthenticationError,
    IllegalMoveError,
)


def handle_user_login(socket, params):
    name = params.get('name', '')
    try:
        socket.user.name = socket.manager.authenticate(name)
        socket.user.update_state()
    except AuthenticationError as error:
        socket.send(MESSAGE_USER_LOGIN_ERROR, {'detail': error.args[0]})
    else:
        socket.manager.update_state()


def handle_game_create(socket, params):
    socket.manager.create_game(socket.user, params['side'])


def handle_game_join(socket, params):
    game = socket.manager.games[params['id']]
    game.join(socket.user, params['side'])
    socket.manager.update_state()


def handle_game_move(socket, params):
    assert params['side'] in {'black', 'white'}
    assert socket.user.game

    game = socket.user.game
    try:
        game.make_move(params['x'], params['y'], params['side'])
    except IllegalMoveError:
        socket.send(MESSAGE_GAME_ERROR, {'detail': 'Illegal move'})
    else:
        socket.manager.update_state()


def handle_game_leave(socket, params=None):
    game = socket.user.game
    if not game:
        socket.send(MESSAGE_GAME_ERROR, {'detail': 'You are not in the game'})
    else:
        game.leave(socket.user)
        socket.manager.update_state()
