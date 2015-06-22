# coding: utf-8
EMPTY = 0
PLAYER_BLACK = 1
PLAYER_WHITE = 2
PLAYERS = {PLAYER_BLACK, PLAYER_WHITE}


class Board:

    def __init__(self, size=15):
        self._board = [[0 for x in range(size)] for y in range(size)]
        self.size = size

    def __check_bounds(self, x, y):
        if (
            x < 0 or x >= self.size or
            y < 0 or y >= self.size
        ):
            raise IndexError('Index out of bounds [{0}, {1}]'.format(x, y))

    def get(self, x, y):
        self.__check_bounds(x, y)
        return self._board[x][y]

    def set(self, x, y, value):
        self.__check_bounds(x, y)
        self._board[x][y] = value

    def to_json(self):
        return self._board

    def is_winning(self, x, y):
        """Check if tile is a part of a winning row"""
        player = self.get(x, y)

        if not player:
            return False

        def total_adjacent(dir, x, y, total=0):
            try:
                pos, value = self.adjacent(dir, x, y)
            except IndexError:
                return total
            if value == player:
                return total_adjacent(dir, pos[0], pos[1], total + 1)
            return total

        return (
            total_adjacent('u', x, y) + total_adjacent('d', x, y) == 4 or
            total_adjacent('l', x, y) + total_adjacent('r', x, y) == 4 or
            total_adjacent('ur', x, y) + total_adjacent('dl', x, y) == 4 or
            total_adjacent('ul', x, y) + total_adjacent('dr', x, y) == 4
        )

    def adjacent(self, dir, x, y):
        """
        Get value of an adjacent cell.

        Direction is specified by a string combination of letters:
            'u' - up
            'd' - down
            'l' - left
            'r' - right

        :param dir: direction
        :param x: x coordinate of starting cell
        :param y: y coordinate of starting cell
        :return: a tuple of (x, y, value)
        """
        if 'u' in dir:
            x -= 1
        elif 'd' in dir:
            x += 1

        if 'l' in dir:
            y -= 1
        elif 'r' in dir:
            y += 1

        return (x, y), self.get(x, y)

    def update(self, *items):
        """Bulk update method for testing purposes"""
        for (x, y, value) in items:
            self._board[x][y] = value
