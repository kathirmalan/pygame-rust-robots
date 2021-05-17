import random
from time import sleep
from typing import List

from src import util
from src.body import SimpleBody
from src.game_board import GameBoard
from src.position import Position
from src.robot import Robot
from src.ui_board import show_startup_board, update_board
from src.weapon import BasicWeapon


def print_team_playing(team_name):
    msg = f"[{team_name.title()}] playing..."
    print(msg)


def get_opponent_team_name(teams, current_team_name):
    # teams = ['blue', 'red']
    return (set(teams) - {current_team_name}).pop()


def print_robots_position(robots, team):
    positions = [(robot.position.i, robot.position.j) for robot in robots]
    print(f"[{team.title()}] positions = {positions}")


class GameState(object):

    def __init__(self, rows=6, cols=6, num_of_robots_in_each_team=1, num_deactivated_robots=8,
                 can_place_robots_anywhere_when_starting=False):

        self.game_board = GameBoard(rows, cols)
        self.num_of_robots_in_each_team = num_of_robots_in_each_team
        self.num_deactivated_robots = num_deactivated_robots

        self.cells_state = [[None] * cols for _ in range(rows)]  # Will contain object of class or either
        # `Robot`:
        # `Body`
        # `Weapon`
        # otherwise None

        self.blue_team: List[Robot] = []
        self.red_team: List[Robot] = []
        self.deactivated_robots: List[Robot] = []

        # False means can place only on their starting position
        self.can_place_any_where = can_place_robots_anywhere_when_starting
        self.ui_board = None

    def simulate_play(self):
        # pdb.set_trace()
        self.create_new_game()

        # Update UI
        self.ui_board = show_startup_board(self.cells_state, self.game_board)

        teams = ['blue', 'red']
        pick_team_name_to_start = random.choice(teams)
        print_team_playing(pick_team_name_to_start)
        played_msg = self.play_for_team_name(pick_team_name_to_start)

        opponent_team = get_opponent_team_name(teams, pick_team_name_to_start)
        while played_msg == 'continue':
            print_team_playing(opponent_team)
            played_msg = self.play_for_team_name(opponent_team)
            opponent_team = get_opponent_team_name(teams, opponent_team)

        return played_msg

    def play_for_team_name(self, team_name):
        if team_name == 'blue':
            return self.play_team(self.blue_team, team_name)
        else:
            return self.play_team(self.red_team, team_name)

    def create_new_game(self):
        self.create_blue_team(self.num_of_robots_in_each_team)
        self.create_red_team(self.num_of_robots_in_each_team)
        deactivated_robots_positions = self.get_positions_for_deactivated_robots()
        self.create_deactivated_robots(deactivated_robots_positions)

    def create_blue_team(self, num_of_robots):
        team_name = 'blue'
        num_of_robots = min(num_of_robots, self.game_board.cols)

        possible_row_positions = [0]
        if self.can_place_any_where:
            possible_row_positions = list(range(self.game_board.rows // 2))

        for _ in range(num_of_robots):
            position = self.game_board.generate_random_col_position(row_position=random.choice(possible_row_positions))
            robot = Robot(
                team_name=team_name,
                position=position,
                game_board=self.game_board,
                body=SimpleBody(),
                weapon=BasicWeapon(self.game_board),
                weapon_slots_count=1,
                movement_count=1,
                is_active=True
            )
            self.cells_state[position.i][position.j] = robot
            self.blue_team.append(robot)

    def create_red_team(self, num_of_robots):
        team_name = 'red'
        num_of_robots = min(num_of_robots, self.game_board.cols)

        possible_row_positions = [self.game_board.rows - 1]
        if self.can_place_any_where:
            possible_row_positions = list(range(self.game_board.rows // 2, self.game_board.rows))

        for _ in range(num_of_robots):
            position = self.game_board.generate_random_col_position(row_position=random.choice(possible_row_positions))
            robot = Robot(
                team_name=team_name,
                position=position,
                game_board=self.game_board,
                body=SimpleBody(),
                weapon=BasicWeapon(self.game_board),
                weapon_slots_count=1,
                movement_count=1,
                is_active=True
            )
            self.cells_state[position.i][position.j] = robot
            self.red_team.append(robot)

    def get_positions_for_deactivated_robots(self) -> List[Position]:
        num_deactivated_robots = self.num_deactivated_robots

        possible_positions_for_deactive_robot = []
        for i in range(1, self.game_board.rows - 1):
            for j in range(self.game_board.cols):
                if self.cells_state[i][j] is None:
                    possible_positions_for_deactive_robot.append(Position(i, j))

        # pdb.set_trace()
        return random.sample(possible_positions_for_deactive_robot, num_deactivated_robots)

    def create_deactivated_robots(self, deactivated_robots_positions: List[Position]):
        for position in deactivated_robots_positions:
            robot = Robot(
                team_name=None,
                position=position,
                game_board=self.game_board,
                body=None,
                weapon=None,
                weapon_slots_count=0,
                movement_count=0,
                is_active=False
            )
            self.cells_state[position.i][position.j] = robot
            self.deactivated_robots.append(robot)

    def play_team(self, team_members, team_name):
        at_least_one_robot_made_move = False
        robots_with_completed_moves: List[Robot] = []
        # Because the play is random we may kill our own team member robot
        while True:
            robot = self.get_robot_to_make_move(robots_with_completed_moves, team_members)
            if robot is None:
                break
            robot.print_position()

            move_status: bool = robot.play_random_move(self.cells_state)

            print("*" * 51)
            print(f"Blue = {len(self.blue_team)}")
            print(f"Red = {len(self.red_team)}")
            print(f"Deactive = {len(self.deactivated_robots)}")

            update_board(self.cells_state, self.ui_board)
            sleep(util.SLEEP_TIME_FOR_BOARD_UPDATE)

            at_least_one_robot_made_move |= move_status
            robots_with_completed_moves.append(robot)
            self.update_all_team_members()
            if team_name == 'blue' and len(self.red_team) == 0:
                print_robots_position(self.red_team, 'bw-red')
                print_robots_position(self.blue_team, 'bw-blue')
                return 'blue'
            if team_name == 'red' and len(self.blue_team) == 0:
                print_robots_position(self.blue_team, 'rw-blue')
                print_robots_position(self.red_team, 'rw-red')
                return 'red'

        if not at_least_one_robot_made_move:
            print_robots_position(self.blue_team, 'bblue')
            print_robots_position(self.red_team, 'rred')
            return 'blue' if team_name == 'red' else 'red'
        return 'continue'

    def get_robot_to_make_move(self, robots_with_completed_moves, team_robots):

        for robot in team_robots:
            if robot not in robots_with_completed_moves:
                return robot
        return None

    def update_all_team_members(self):

        cells_state = self.cells_state
        self.blue_team = []
        self.red_team = []
        self.deactivated_robots = []

        for i in range(self.game_board.rows):
            for j in range(self.game_board.cols):
                cell_obj = cells_state[i][j]
                if cell_obj is None:
                    continue
                if isinstance(cell_obj, Robot):
                    self.add_robot_in_team(cell_obj)

    def add_robot_in_team(self, robot):
        if robot.team_name == 'blue':
            self.blue_team.append(robot)
        elif robot.team_name == 'red':
            self.red_team.append(robot)
        else:
            self.deactivated_robots.append(robot)
