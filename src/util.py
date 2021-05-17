import pdb
import random
import os

from src.position import Position

# *********************   Set Game Configuration
ROWS = COLS = 8
ROBOTS_IN_EACH_TEAM = 2
# False: starting position of robots will be at their respective row i.e. first for BLUE and last for the RED
# True: this allows the simulation to place robots anywhere but limited to top-half for the BLUE and bottom-half for RED
CAN_RANDOMLY_PLACE_ROBOT_ANYWHERE_ON_STARTING = False
NUMBER_OF_GAMES_FOR_SIMULATION = 5
SLEEP_TIME_FOR_BOARD_UPDATE = 2

# Teams = {'blue', 'red'}
TEAMS = ['blue', 'red']


def get_project_dir():
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def get_assets_dir():
    return os.path.join(get_project_dir(), 'assets')


def get_fonts_dir():
    return os.path.join(get_assets_dir(), 'fonts')


def get_asset_fullpath(fname):
    return os.path.join(get_assets_dir(), fname)


def get_font_fullpath(fontname):
    return os.path.join(get_fonts_dir(), fontname)


def get_board_rows_cols():
    return ROWS, COLS


def get_number_of_robots_in_each_team():
    return ROBOTS_IN_EACH_TEAM


def get_count_of_deactivated_robots(rows, cols):
    return int((rows * cols) / 4 - 1)
