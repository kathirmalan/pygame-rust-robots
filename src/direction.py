import pdb
import random

from src.game_board import GameBoard
from src.position import Position


class Direction(object):
    """
    Direction:
        north: 0
        east: 1
        south: 2
        west: 3
    """

    DIRECTIONS = ('north', 'east', 'south', 'west')

    # Left-Right-Forward-Backward when facing: north, south, east, west
    # lrfb: stands for first letter from ['left', 'right', 'forward', 'backward'
    DIRECTIONS_LRFB_MAP = {
        'north': {'left': 'west', 'right': 'east', 'forward': 'north', 'backward': 'south'},
        'south': {'left': 'east', 'right': 'west', 'forward': 'south', 'backward': 'north'},
        'east': {'left': 'north', 'right': 'south', 'forward': 'east', 'backward': 'west'},
        'west': {'left': 'south', 'right': 'north', 'forward': 'west', 'backward': 'east'}

    }

    @staticmethod
    def get_nth_cell(from_position, nth, in_direction):
        direction = in_direction
        ith_pos, jth_pos = None, None
        if direction == 'north':
            ith_pos = from_position.i - nth
            jth_pos = from_position.j
        elif direction == 'south':
            ith_pos = from_position.i + nth
            jth_pos = from_position.j
        elif direction == 'east':
            ith_pos = from_position.i
            jth_pos = from_position.j + nth
        elif direction == 'west':
            ith_pos = from_position.i
            jth_pos = from_position.j - nth

        return Position(ith_pos, jth_pos)

    @staticmethod
    def get_num_cells_impactable(position: Position, game_board: GameBoard, in_direction: str) -> int:

        direction = in_direction

        num_of_cells_impactable = 0
        if direction == 'north':
            num_of_cells_impactable = position.i  #
        elif direction == 'south':
            num_of_cells_impactable = game_board.rows - position.i - 1  # -1: Because indexing starts from 0
        elif direction == 'east':
            num_of_cells_impactable = game_board.cols - position.j - 1
        elif direction == 'west':
            num_of_cells_impactable = position.j

        return num_of_cells_impactable

    def __init__(self, direction: str):
        self.direction = direction

    def set_direction(self, direction: str):
        self.direction = direction

    def nth_cell(self, from_position: Position, nth: int) -> Position:
        return Direction.get_nth_cell(from_position, nth, self.direction.lower())

    def get_nth_cell_in_lrfb(self, from_position: Position, nth: int, lrfb: str) -> Position:
        """
        lrfb: is from ['left', 'right', 'forward', 'backward'
        """
        return Direction.get_nth_cell(from_position, nth, self.get_lrfb_direction(lrfb))

    def num_cells_impactable(self, position: Position, game_board: GameBoard) -> int:
        return Direction.get_num_cells_impactable(position, game_board, self.direction.lower())

    def num_cells_impactable_in_lrfb(self, position: Position, game_board: GameBoard, lrfb: str):
        return Direction.get_num_cells_impactable(position, game_board, self.get_lrfb_direction(lrfb))

    def get_lrfb_direction(self, lrfb: str) -> str:
        return Direction.DIRECTIONS_LRFB_MAP[self.direction.lower()][lrfb.lower()]

    @staticmethod
    def get_random_direction():
        return random.choice(Direction.DIRECTIONS)
