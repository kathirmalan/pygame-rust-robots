import random
from typing import List

from src.body import Body, choose_body, SimpleBody
from src.direction import Direction
from src.game_board import GameBoard
from src.position import Position
from src.weapon import Weapon, BasicWeapon, choose_weapon, WeaponSlots


def get_initial_direction(team_name):
    """
    Direction:
        north: 0
        east: 1
        south: 2
        west: 3
    """

    if team_name is None:
        return None

    team_name = team_name.lower()
    team_wise_initial_facing_direction = {
        'blue': Direction('south'),  # First Line i.e from Top-Left
        'red': Direction('north')  # Last Line i.e
    }
    return team_wise_initial_facing_direction[team_name]


def filter_non_empty_cells(reachable_moves_position, cells_state):
    can_move_positions = []
    for position in reachable_moves_position:
        cell_object = cells_state[position.i][position.j]
        if cell_object is None or isinstance(cell_object, (Body, Weapon)):
            can_move_positions.append(position)
    return can_move_positions


def get_random_move(moves: List[Position]):
    if len(moves) > 0:
        return random.choice(moves)
    else:
        return None


def should_change_face_direction():
    return random.randint(0, 1)


def get_random_body_or_weapon(game_board):
    body_or_weapon = random.choice(['body', 'weapon'])

    if body_or_weapon == 'body':
        return choose_body()
    else:
        return choose_weapon(game_board)


class Robot(object):

    def __init__(self,
                 team_name,
                 position,
                 game_board,
                 body=SimpleBody(),
                 weapon=BasicWeapon(GameBoard(6, 6)),
                 weapon_slots_count=1,
                 movement_count=1,
                 is_active=True):
        """
        team_name:
            'blue', 'red'
        """
        self.team_name = team_name.lower() if team_name is not None else team_name
        self.face_direction = get_initial_direction(self.team_name)
        self.position = position
        self.game_board = game_board

        self.enabled_body: Body = body
        self.enabled_weapon_slots: WeaponSlots = WeaponSlots(weapon_slots_count, [weapon])

        self.remaining_bodies: List[Body] = []
        self.remaining_weapons: List[Weapon] = []

        self.movement_count = movement_count

        self.is_active = is_active

    def play_random_move(self, cells_state) -> bool:
        """
        cells_state: Will contain object of class or either
                        `Robot`:
                        `Body`
                        `Weapon`
                        otherwise None
        """
        # Get possible move
        # Move,
        #   if not possible, return False
        # Add body or weapon if found
        # Reduce movement count
        # Change Face Direction: can change but necessarily have to
        # Use weapons in slots: only use one from the enabled weapons given enough hp
        # update, enabled-body , change-body, change weapons in weapon-slots

        # pdb.set_trace()

        if self.movement_count == 0:
            return False  # Because robot can not move

        reachable_positions: List[Position] = self.get_possible_moves()
        can_move_positions = filter_non_empty_cells(reachable_positions, cells_state)
        picked_random_move_position = get_random_move(can_move_positions)
        if picked_random_move_position is None:
            return False  # Indicating can not move

        # Reduce movement count
        self.movement_count -= 1

        # Move
        cells_state[self.position.i][self.position.j] = None
        self.position = picked_random_move_position
        cells_state[picked_random_move_position.i][picked_random_move_position.j] = self

        # Add body or weapon if found
        if cells_state[picked_random_move_position.i][picked_random_move_position.j] is not None:
            self.add_body_or_weapon_found(picked_random_move_position, cells_state)

        if should_change_face_direction():
            self.change_face_direction()

        health_points_available = self.get_health_point_from_enabled_body()

        # Using weapon completes the move
        picked_weapon = self.pick_random_weapon(health_points_available)
        if picked_weapon is None:
            return True  # Because made a move but can not use weapon either no health-point available

        self.use_weapon(picked_weapon, cells_state)

        self.use_health_point(picked_weapon.health_point_required)
        # self.enabled_weapon_slots.remove(used_weapon) # Weapons remains forever
        # update body
        # Remove body if no health-point and Change for sure
        # Change Body # Can choose to not change
        self.update_bodies()
        # update weapons-slot
        # Change weapons in Weapon-slot
        self.update_weapons()

        # Iterate through cells and update teams-robots, deactivated robots
        return True

    def get_possible_moves(self) -> List[Position]:
        possible_moves: List[Position] = [
            # North w.r.t board
            Position(self.position.i - 1, self.position.j),
            # South
            Position(self.position.i + 1, self.position.j),
            # East
            Position(self.position.i, self.position.j + 1),
            # West
            Position(self.position.i, self.position.j - 1)
        ]
        reachable_moves: List[Position] = self.game_board.remove_unreachable_cells(possible_moves)
        return reachable_moves

    def add_body_or_weapon_found(self, position: Position, cells_state):
        cell_obj = cells_state[position.i][position.j]
        if isinstance(cell_obj, Body):
            self.enabled_weapon_slots.increment_count(cell_obj.weapon_slots)
            self.movement_count += cell_obj.movement_point
            self.remaining_bodies.append(cell_obj)
        elif isinstance(cell_obj, Weapon):
            if cell_obj.get_num_weapon_slots() > 0:
                self.enabled_weapon_slots.increment_count(cell_obj.get_num_weapon_slots())
                if len(cell_obj.get_impacted_cells(position,
                                                   self.face_direction)) == 0:  # If the weapon has no impact factor then no need to add.
                    return
            did_add_weapon_in_available_slot = self.enabled_weapon_slots.add(cell_obj)
            if not did_add_weapon_in_available_slot:
                self.remaining_weapons.append(cell_obj)

    def change_face_direction(self):
        self.face_direction.set_direction(random.choice(Direction.DIRECTIONS))

    def get_health_point_from_enabled_body(self):
        return self.enabled_body.health_point

    def pick_random_weapon(self, health_points_available: int) -> Weapon:
        return self.enabled_weapon_slots.choose_random_weapon(health_points_available)

    def use_weapon(self, picked_weapon: Weapon, cells_state):
        cells_impacted_positions: List[Position] = picked_weapon.get_impacted_cells(self.position, self.face_direction)
        for position in cells_impacted_positions:
            cell_obj = cells_state[position.i][position.j]
            if cell_obj is None:
                continue
            if isinstance(cell_obj, Robot):
                cells_state[position.i][position.j] = get_random_body_or_weapon(self.game_board)
                del cell_obj  # delete cell object
            # TODO: If there is Body or Weapon then it will be left as it is.

    def use_health_point(self, health_point):
        self.enabled_body.use_health_point(health_point)

    def update_bodies(self):
        # update body
        # Remove body if no health-point and Change for sure
        # Change Body # Can choose to not change
        body: Body = self.randomly_select_a_body()
        if body is None:
            return None

        if self.enabled_body.health_point == 0:
            self.enabled_body = body
            self.remaining_bodies.remove(body)
            return

        # pdb.set_trace()
        if random.randint(0, 1):
            used_enabled_body = self.enabled_body
            self.enabled_body = body
            self.remaining_bodies.remove(body)
            self.remaining_bodies.append(used_enabled_body)

    def update_weapons(self):
        available_weapons = self.get_all_weapons()
        slots = self.enabled_weapon_slots.count()

        weapons_tobe_enabled = random.sample(available_weapons, min(slots, len(available_weapons)))
        self.enabled_weapon_slots = WeaponSlots(slots, weapons_tobe_enabled)
        self.remaining_weapons = []
        for weapon in available_weapons:
            if weapon not in weapons_tobe_enabled:
                self.remaining_weapons.append(weapon)
        return

    def get_all_weapons(self):
        weapons = self.enabled_weapon_slots.get_weapons()
        remaining_weapons = self.remaining_weapons
        return weapons + remaining_weapons

    def randomly_select_a_body(self):
        if len(self.remaining_bodies) > 0:
            return random.choice(self.remaining_bodies)
        return None  # means can not change body

    def deactivate(self):
        self.is_active = False

    def print_position(self):
        print(f"[{self.team_name}] robot position = ({self.position.i}, {self.position.j})")
