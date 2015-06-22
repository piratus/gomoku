# coding: utf-8
from unittest import TestCase
from unittest.mock import patch

from gomoku.game.exceptions import AuthenticationError
from gomoku.game.manager import Manager
from gomoku.game.tests.utils import mock_socket


class ManagerTestCase(TestCase):

    def test_disconnect(self):
        manager = Manager()
        user = manager.connect(mock_socket())
        game = manager.create_game(user, 'black')

        self.assertEqual(1, len(manager.users))
        self.assertEqual(1, len(manager.games))

        self.assertEqual(game, user.game)
        self.assertEqual(user, game.players['black'])

        manager.disconnect(user._socket)
        self.assertEqual(0, len(manager.users))
        self.assertEqual(0, len(manager.games))

        self.assertIsNone(user.game)
        self.assertIsNone(game.players['black'])
        self.assertIsNone(user._socket)

    def test_connect_disconnect(self):
        manager = Manager()

        socket1 = mock_socket()
        with patch.object(manager, 'update_state') as update_state:
            manager.connect(socket1)
            self.assertIn(socket1, manager.users)
            self.assertTrue(update_state.called)

        socket2 = mock_socket()
        with patch.object(manager, 'update_state') as update_state:
            manager.connect(socket2)
            self.assertIn(socket1, manager.users)
            self.assertIn(socket2, manager.users)
            self.assertTrue(update_state.called)

        with patch.object(manager, 'update_state') as update_state:
            manager.disconnect(socket2)
            self.assertNotIn(socket2, manager.users)
            self.assertIn(socket1, manager.users)
            self.assertTrue(update_state.called)

        with patch.object(manager, 'update_state') as update_state:
            manager.disconnect(socket1)
            self.assertNotIn(socket1, manager.users)
            self.assertNotIn(socket2, manager.users)
            self.assertTrue(update_state.called)

        with patch.object(manager, 'update_state') as update_state:
            manager.disconnect(socket1)
            self.assertFalse(update_state.called)

    def test_authenticate(self):
        users = Manager()

        user = users.connect(mock_socket())
        user.name = users.authenticate('piratus')

        user2 = users.connect(mock_socket())

        with self.assertRaises(AuthenticationError):
            user2.name = users.authenticate(None)

        with self.assertRaises(AuthenticationError):
            user2.name = users.authenticate('')

        with self.assertRaises(AuthenticationError):
            user2.name = users.authenticate('piratus')

        with self.assertRaises(AuthenticationError):
            user2.name = users.authenticate('  piratus')

        self.assertEqual('', user2.name)

        user2.name = users.authenticate('username')
        self.assertEqual('piratus', user.name)
        self.assertEqual('username', user2.name)

    def test_create_game(self):
        manager = Manager()
        user = manager.connect(mock_socket())
        user.name = manager.authenticate('piratus')
        manager.create_game(user, 'black')
