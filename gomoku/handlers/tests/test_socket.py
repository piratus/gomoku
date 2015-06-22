# coding: utf-8
import json
from unittest import TestCase
from unittest.mock import Mock, MagicMock

from gomoku.handlers.socket import SocketHandler


class SampleException(Exception):
    pass


class SocketHandlerTestCase(TestCase):

    def setUp(self):
        self.socket = SocketHandler(MagicMock(), MagicMock())
        self.socket.write_message = Mock()

    def test_send(self):

        self.socket.send('MESSAGE_NAME', {'key': 'value'})
        self.socket.write_message.assert_called_with({
            'MESSAGE': 'MESSAGE_NAME',
            'BODY': {'key': 'value'}
        })

    def test_send_empty(self):
        self.socket.send('EMPTY_MESSAGE')
        self.socket.write_message.assert_called_with({
            'MESSAGE': 'EMPTY_MESSAGE'
        })

    def test_on_message(self):
        handler = MagicMock()
        empty_handler = MagicMock()
        self.socket.handlers = {'name': handler, 'empty': empty_handler}

        self.socket.on_message(json.dumps({
            'MESSAGE': 'name',
            'BODY': {'key': 'value'}
        }))

        handler.assert_called_with(self.socket, {'key': 'value'})

        self.socket.on_message(json.dumps({'MESSAGE': 'empty'}))
        empty_handler.assert_called_with(self.socket, None)

    def test_on_message_bad(self):
        self.socket.on_message(json.dumps({'BODY': 'no message name'}))
        self.socket.on_message('Just a string')

    def test_on_message_unknown(self):
        self.socket.on_message(json.dumps({'MESSAGE': 'does-not-exist'}))
        self.socket.on_message('Just a string')

    def test_on_message_handler_exception(self):
        handler = MagicMock(side_effect=SampleException())
        self.socket.handlers = {'ERROR': handler}
        self.socket.on_message(json.dumps({'MESSAGE': 'ERROR'}))
