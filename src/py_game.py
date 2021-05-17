import pdb
from src import util
from src.game_state import GameState
from src.ui_board import exit_func


def py_game_simulation():
    rows, cols = get_board_rows_cols()
    num_of_robots_in_each_team = get_number_of_robots_in_each_team()
    num_of_deactivated_robots = get_count_of_deactivated_robots(rows, cols)
    can_place_robots_anywhere_when_starting = util.CAN_RANDOMLY_PLACE_ROBOT_ANYWHERE_ON_STARTING
    number_of_games_for_simulation = util.NUMBER_OF_GAMES_FOR_SIMULATION

    i = 0
    while True:
        new_game_state: GameState = create_new_game(rows,
                                                    cols,
                                                    num_of_robots_in_each_team,
                                                    num_of_deactivated_robots,
                                                    can_place_robots_anywhere_when_starting)
        return_msg = new_game_state.simulate_play()
        print_winner_message(return_msg)
        i += 1
        if i == number_of_games_for_simulation:
            break
    print_completion_message()
    exit_func()
    return


def get_board_rows_cols():
    return util.get_board_rows_cols()


def get_number_of_robots_in_each_team():
    return util.get_number_of_robots_in_each_team()


def get_count_of_deactivated_robots(rows, cols):
    return util.get_count_of_deactivated_robots(rows, cols)


def create_new_game(rows, cols, num_of_robots_in_each_team, num_of_deactivated_robots,
                    can_place_robots_anywhere_when_starting) -> GameState:
    new_game_state = GameState(rows, cols, num_of_robots_in_each_team, num_of_deactivated_robots,
                               can_place_robots_anywhere_when_starting)
    return new_game_state


def print_winner_message(winner_team_name):
    print("**********************************")
    print(f"##     {winner_team_name.title()} Won     ##")
    print("**********************************")


def print_completion_message():
    msg = """
    ****************************************
    ##        Everything Completed        ##
    ****************************************
    """
    print(msg)
