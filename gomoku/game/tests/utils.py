# coding: utf-8
from unittest.mock import MagicMock, Mock


def mock_socket(send=None):
    socket = MagicMock()
    socket.send = send or Mock()
    return socket
