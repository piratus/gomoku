# coding: utf-8
from unittest import TestCase
from unittest.mock import Mock, patch

from gomoku.constants import MESSAGE_USER_UPDATE_STATE
from gomoku.game.tests.utils import mock_socket
from gomoku.game.users import User


class UserTestCase(TestCase):

    def test_auth(self):
        socket = mock_socket()
        user = User(socket)
        self.assertFalse(user.is_authenticated)
        self.assertFalse(socket.send.called)

        user.name = 'piratus'
        self.assertTrue(user.is_authenticated)
        self.assertEqual(MESSAGE_USER_UPDATE_STATE,
                         socket.send.call_args[0][0])

    @patch('gomoku.game.users.uuid4', Mock(return_value='uuid'))
    def test_to_json(self):
        user = User(name='piratus')
        self.assertEqual(user.to_json(), {
            'id': 'uuid',
            'name': 'piratus',
            'isAuthenticated': True,
            'game': None,
            'side': None,
        })
        self.assertEqual(user.to_json(short=True), {
            'id': 'uuid',
            'name': 'piratus',
        })

    def test_update_state(self):
        socket = mock_socket()

        user = User(socket, 'piratus')
        user.update_state()

        socket.send.assert_called_with(
            MESSAGE_USER_UPDATE_STATE,
            {'user': user.to_json()}
        )
