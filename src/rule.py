import pdb

from src.position import Position


def get_possible_moves(self, pos):
    i, j = pos.i, pos.j

    # Top, Right, Bottom, Left
    possible_moves = [Position(i - 1, j), Position(i, j + 1), Position(i + 1, j), Position(i, j - 1)]

    return possible_moves
