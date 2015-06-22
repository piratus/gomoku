# coding: utf-8
from datetime import datetime
from unittest import TestCase
from unittest.mock import patch, Mock

from gomoku.constants import GameState
from gomoku.game.exceptions import IllegalMoveError
from gomoku.game.game import Game
from gomoku.game.tests.utils import mock_socket
from gomoku.game.users import User


class GameTestCase(TestCase):

    def test_join(self):
        game = Game()
        self.assertIsNone(game.players['black'])
        self.assertIsNone(game.players['white'])

        user1 = User(mock_socket())
        game.join(user1, 'black')
        self.assertEqual(GameState.WAITING, game.state)
        self.assertEqual(game, user1.game)
        self.assertEqual(user1, game.players['black'])
        self.assertIsNone(game.players['white'])

        game.join(user1, 'white')
        self.assertEqual(GameState.WAITING, game.state)
        self.assertEqual(game, user1.game)
        self.assertEqual(user1, game.players['white'])
        self.assertIsNone(game.players['black'])

        new_game = Game()
        new_game.join(user1, 'black')
        self.assertEqual(new_game, user1.game)
        self.assertEqual(user1, new_game.players['black'])
        self.assertIsNone(game.players['black'])
        self.assertIsNone(game.players['white'])

    @patch('gomoku.game.game.uuid4', Mock(return_value='id'))
    @patch('gomoku.game.users.uuid4', Mock(return_value='uid'))
    def test_to_json(self):
        game = Game()
        game.notify_players = Mock()
        self.assertEqual(game.to_json(), {
            'id': 'id',
            'state': 0,
            'turn': 'black',
            'black': None,
            'white': None,
            'started': None,
            'winner': None,
            'board': None,
        })

        with patch('gomoku.game.game.datetime') as datetime_mock:
            datetime_mock.now.return_value = datetime(2015, 1, 1)
            datetime_mock.side_effect = lambda *a, **k: datetime(*a, **k)

            game.join(User(name='piratus'), 'black')
            game.join(User(name='not_piratus'), 'white')

        json = game.to_json()

        board = json.pop('board')
        self.assertEqual(15, len(board))
        for x in range(15):
            self.assertEqual(15, len(board[x]))
        self.assertEqual(json, {
            'id': 'id',
            'state': 2,
            'turn': 'black',
            'black': {'id': 'uid', 'name': 'piratus'},
            'white': {'id': 'uid', 'name': 'not_piratus'},
            'winner': None,
            'started': '2015-01-01 00:00:00',
        })

    def test_make_move(self):
        game = Game()
        game.notify_players = Mock()

        self.assertEqual('black', game.turn)

        player1 = User(name='piratus')
        game.join(player1, 'black')

        with self.assertRaises(IllegalMoveError):
            game.make_move(0, 0, 'black')

        player2 = User(name='not-piratus')
        game.join(player2, 'white')

        game.make_move(0, 0, 'black')
        self.assertIsNone(game.winner)
        self.assertEqual('white', game.turn)

        with self.assertRaises(IllegalMoveError):
            game.make_move(0, 1, 'black')

        with self.assertRaises(IllegalMoveError):
            game.make_move(15, 15, 'white')

        game.make_move(14, 14, 'white')
        self.assertIsNone(game.winner)

        game.make_move(1, 0, 'black')
        game.make_move(13, 13, 'white')

        game.make_move(2, 0, 'black')
        game.make_move(12, 12, 'white')

        game.make_move(3, 0, 'black')
        game.make_move(11, 11, 'white')

        game.make_move(4, 0, 'black')

        self.assertEqual('black', game.winner)
        self.assertEqual(GameState.FINISHED, game.state)

        with self.assertRaises(IllegalMoveError):
            game.make_move(10, 10, 'white')

        game.leave(player2)
        self.assertEqual(GameState.FINISHED, game.state)
