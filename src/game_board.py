import pdb
from random import randrange
from typing import List

from src.position import Position


class GameBoard(object):

    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols

    def remove_unreachable_cells(self, positions: List[Position]):

        reachable_cells = []
        for position in positions:
            if self.is_row_pos_satisfied(position.i) & self.is_col_pos_satisfied(position.j):
                reachable_cells.append(position)

        return reachable_cells

    def is_row_pos_satisfied(self, row_pos):
        return (row_pos >= 0) & (row_pos < self.rows)

    def is_col_pos_satisfied(self, col_pos):
        return (col_pos >= 0) & (col_pos < self.rows)

    def generate_random_cell_position(self) -> Position:
        return Position(randrange(self.rows), randrange(self.cols))

    def generate_random_col_position(self, row_position):
        return Position(row_position, randrange(self.cols))

    def generate_random_row_position(self, col_position):
        return Position(randrange(self.rows), col_position)
