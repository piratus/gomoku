# coding: utf-8
from unittest import TestCase

from gomoku.game.board import (
    Board,
    EMPTY,
    PLAYER_BLACK,
    PLAYER_WHITE,
)
from gomoku.game.exceptions import IllegalMoveError


class BoardTestCase(TestCase):

    def test_get(self):
        board = Board()
        self.assertEqual(EMPTY, board.get(0, 0))

        with self.assertRaises(IndexError):
            board.get(-1, 1)

        with self.assertRaises(IndexError):
            board.get(1, -1)

        with self.assertRaises(IndexError):
            board.get(15, 5)

        with self.assertRaises(IndexError):
            board.get(5, 15)

    def test_set(self):
        board = Board()
        board.set(0, 0, PLAYER_BLACK)
        self.assertEqual(PLAYER_BLACK, board.get(0, 0))

        board.set(14, 14, PLAYER_WHITE)
        self.assertEqual(PLAYER_WHITE, board.get(14, 14))

        with self.assertRaises(IndexError):
            board.set(-1, 4, PLAYER_WHITE)

        with self.assertRaises(IndexError):
            board.set(1, 15, PLAYER_BLACK)

    def test_to_json(self):
        board = Board()
        for x in range(15):
            for y in range(15):
                board.set(x, y, x)

        self.assertEqual(
            [[x] * 15 for x in range(15)],
            board.to_json()
        )

    def test_winner_check(self):
        board = Board()
        board.update(
            (0, 0, 1), (1, 0, 1), (2, 0, 1), (3, 0, 1), (4, 0, 1),
            (1, 1, 2), (2, 2, 2), (3, 3, 2), (4, 4, 2), (5, 5, 2),
        )

        self.assertFalse(board.is_winning(0, 2), 'Empty cell')
        self.assertTrue(board.is_winning(0, 0), 'Black vertical')
        self.assertTrue(board.is_winning(1, 1), 'White diagonal')

    def test_adjacent(self):
        board = Board()
        board.update(
            (0, 1, 1), (0, 2, 2), (1, 2, 3), (2, 2, 4),
            (2, 1, 5), (2, 0, 6), (1, 0, 7), (0, 0, 8),
        )

        self.assertEqual(((0, 1), 1), board.adjacent('u', 1, 1))
        self.assertEqual(((0, 2), 2), board.adjacent('ur', 1, 1))
        self.assertEqual(((1, 2), 3), board.adjacent('r', 1, 1))
        self.assertEqual(((2, 2), 4), board.adjacent('dr', 1, 1))
        self.assertEqual(((2, 1), 5), board.adjacent('d', 1, 1))
        self.assertEqual(((2, 0), 6), board.adjacent('dl', 1, 1))
        self.assertEqual(((1, 0), 7), board.adjacent('l', 1, 1))
        self.assertEqual(((0, 0), 8), board.adjacent('ul', 1, 1))

        with self.assertRaises(IndexError):
            board.adjacent('u', 0, 0)
