import pdb
import random
from typing import List

from src.direction import Direction
from src.game_board import GameBoard
from src.position import Position


class Weapon(object):

    def __init__(self):
        self.health_point_required = None
        self.game_board = None

    def name(self):
        return self.__class__.__name__

    def get_impacted_cells(self, robo_pos, direction_facing):
        raise Exception("NotImplementedException")

    def get_num_weapon_slots(self):
        return 0


class BasicWeapon(Weapon):

    def __init__(self, game_board):
        super().__init__()
        self.health_point_required = 1
        self.game_board = game_board
        self._num_cells_impactable = 2

    def name(self):
        return self.__class__.__name__

    def get_impacted_cells(self, robo_pos, direction_facing):
        """
        robo_face_direction:
            north -> east -> south -> west
        """
        cells_impacted_positions = []
        for nth in range(self._num_cells_impactable):
            cells_impacted_positions.append(direction_facing.nth_cell(robo_pos, nth + 1))

        reachable_cells: List[Position] = self.game_board.remove_unreachable_cells(cells_impacted_positions)
        return reachable_cells


class LaserWeapon(Weapon):

    def __init__(self, game_board):
        super().__init__()
        self.health_point_required = 1
        self.game_board = game_board

    def name(self):
        return self.__class__.__name__

    def get_impacted_cells(self, robo_pos, direction_facing):
        """
        robo_face_direction:
            top -> right -> bottom -> left
            0, 1, 2, 3

        """
        cells_impacted_positions = []
        num_cells_impactable = direction_facing.num_cells_impactable(robo_pos, self.game_board)

        for nth in range(num_cells_impactable):
            cells_impacted_positions.append(direction_facing.nth_cell(robo_pos, nth + 1))

        reachable_cells = self.game_board.remove_unreachable_cells(cells_impacted_positions)
        return reachable_cells


class SwordWeapon(Weapon):
    """
    Impacts:
        Forward: i.e. direction facing
        Forward-Left:
        Forwar-Right
    """

    def __init__(self, game_board):
        super().__init__()
        self.health_point_required = 2
        self.game_board = game_board

    def name(self):
        return self.__class__.__name__

    def get_impacted_cells(self, robo_pos, direction_facing):
        """
        robo_face_direction:
            top -> right -> bottom -> left
            0, 1, 2, 3

        """

        cells_impacted_positions = []

        # Forward
        forward_position = direction_facing.get_nth_cell_in_lrfb(robo_pos, 1, 'forward')
        cells_impacted_positions.append(forward_position)
        # Forward Left
        forward_left = direction_facing.get_nth_cell_in_lrfb(forward_position, 1, 'left')
        cells_impacted_positions.append(forward_left)
        # Forward Right
        forward_right = direction_facing.get_nth_cell_in_lrfb(forward_position, 1, 'right')
        cells_impacted_positions.append(forward_right)

        reachable_cells: List[Position] = self.game_board.remove_unreachable_cells(cells_impacted_positions)
        return reachable_cells


class ExplosionWeapon(Weapon):
    """
    Impacts:
        * Left, Right, Forward, Backward
        * Forward: Left, Right
        * Backward: Left, Right
    """

    def __init__(self, game_board):
        super().__init__()
        self.health_point_required = 2
        self.game_board = game_board

    def name(self):
        return self.__class__.__name__

    def get_impacted_cells(self, robo_pos, direction_facing):
        """
         robo_face_direction:
             north -> east -> south -> west
         """
        cells_impacted_positions = [direction_facing.get_nth_cell_in_lrfb(robo_pos, 1, 'left'),
                                    direction_facing.get_nth_cell_in_lrfb(robo_pos, 1, 'right')]

        # Forward
        forward_position = direction_facing.get_nth_cell_in_lrfb(robo_pos, 1, 'forward')
        cells_impacted_positions.append(forward_position)

        # Backward
        backward_position = direction_facing.get_nth_cell_in_lrfb(robo_pos, 1, 'backward')
        cells_impacted_positions.append(backward_position)

        # Forward: Left & Right
        cells_impacted_positions.append(direction_facing.get_nth_cell_in_lrfb(forward_position, 1, 'left'))
        cells_impacted_positions.append(direction_facing.get_nth_cell_in_lrfb(forward_position, 1, 'right'))

        # Backward: Left & Right
        cells_impacted_positions.append(direction_facing.get_nth_cell_in_lrfb(backward_position, 1, 'left'))
        cells_impacted_positions.append(direction_facing.get_nth_cell_in_lrfb(backward_position, 1, 'right'))

        reachable_cells: List[Position] = self.game_board.remove_unreachable_cells(cells_impacted_positions)
        return reachable_cells


class DualLaserWeapon(Weapon):

    def __init__(self, game_board):
        super().__init__()
        self.health_point_required = 1
        self.game_board = game_board

    def name(self):
        return self.__class__.__name__

    def get_impacted_cells(self, robo_pos, direction_facing):
        """
         robo_face_direction:
             north -> east -> south -> west
         """

        cells_impacted_positions: List[Position] = []

        # Left Impactable
        left_pos = direction_facing.get_nth_cell_in_lrfb(robo_pos, 1, 'left')
        cells_impacted_positions.append(left_pos)  # 1st added
        num_cells_impactable_left = direction_facing.num_cells_impactable_in_lrfb(left_pos, self.game_board, 'left')
        for nth in range(1, num_cells_impactable_left):
            cells_impacted_positions.append(direction_facing.get_nth_cell_in_lrfb(robo_pos, nth + 1, 'left'))

        # Right Impactable
        right_pos = direction_facing.get_nth_cell_in_lrfb(robo_pos, 1, 'right')
        cells_impacted_positions.append(right_pos)  # 1st added
        right = direction_facing.num_cells_impactable_in_lrfb(right_pos, self.game_board, 'right')
        for nth in range(1, right):
            cells_impacted_positions.append(direction_facing.get_nth_cell_in_lrfb(robo_pos, nth + 1, 'right'))

        reachable_cells: List[Position] = self.game_board.remove_unreachable_cells(cells_impacted_positions)
        return reachable_cells


class TwinWeapon(Weapon):

    def __init__(self, game_board):
        super().__init__()
        self.health_point_required = 1
        self.game_board = game_board
        self._num_cells_impactable = 2

    def name(self):
        return self.__class__.__name__

    def get_impacted_cells(self, robo_pos, direction_facing):
        """
        robo_face_direction:
            top -> right -> bottom -> left
            0, 1, 2, 3

        """
        return []

    def get_num_weapon_slots(self):
        return 2


def choose_weapon(game_board):
    weapons = [BasicWeapon(game_board),
               LaserWeapon(game_board),
               SwordWeapon(game_board),
               ExplosionWeapon(game_board),
               DualLaserWeapon(game_board),
               TwinWeapon(game_board)]

    return random.choice(weapons)


class WeaponSlots(object):

    def __init__(self, slots, weapons):
        self.slots = slots
        self.weapons = weapons

    def count(self):
        return self.slots

    def get_weapons(self):
        return self.weapons

    def set_slots_count(self, count):
        self.slots = count

    def increment_count(self, n=1):
        self.slots += n
        return self.slots

    def decrement_count(self, n=1):
        self.slots -= n
        return self.slots

    def weapons_count(self):
        return len(self.weapons)

    def add(self, weapon: Weapon):
        """If adding is successfull return true
        """
        if self.weapons_count() < self.slots:
            self.weapons.append(weapon)
            self.increment_count()
            return True
        return False

    def remove(self, weapon: Weapon):
        if weapon in self.weapons:
            self.weapons.remove(weapon)
            self.decrement_count()
            return True
        return False

    def choose_random_weapon(self, health_points_available):
        if self.weapons_count() == 0:
            return None

        weapon: Weapon = random.choice(self.weapons)
        if weapon.health_point_required <= health_points_available:
            return weapon

        for weapon in self.weapons:
            if weapon.health_point_required <= health_points_available:
                return weapon

        return None
