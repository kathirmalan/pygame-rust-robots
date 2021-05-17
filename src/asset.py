import os
import pdb

import pygame

from src import util
from src.util import get_asset_fullpath


# Player Icons
def get_player_img(team_name):
    if team_name == 'blue':
        return pygame.image.load(get_asset_fullpath("player_1.png"))
    else:
        return pygame.image.load(get_asset_fullpath("player_2.png"))


def get_direction_img(direction: str, team_name: str):
    """
    Direction:
        north: 0
        east: 1
        south: 2
        west: 3
    """
    if not direction:
        return None

    team_name_idn_dict = {'blue': 2, 'red': 1}
    idn = team_name_idn_dict[team_name]

    if direction == 'north':
        return pygame.image.load(get_asset_fullpath(f"up-p{idn}.png"))

    if direction == 'south':
        return pygame.image.load(get_asset_fullpath(f"down-p{idn}.png"))

    if direction == 'west':
        return pygame.image.load(get_asset_fullpath(f"left-p{idn}.png"))

    if direction == 'east':
        return pygame.image.load(get_asset_fullpath(f"right-p{idn}.png"))


def place_direction_img(direction_img_rect, cell, direction):
    if direction == 'north':
        direction_img_rect.midtop = cell.midtop

    if direction == 'south':
        direction_img_rect.midbottom = cell.midbottom

    if direction == 'west':
        direction_img_rect.midleft = cell.midleft

    if direction == 'east':
        direction_img_rect.midright = cell.midright


def get_body_img():
    return pygame.image.load(get_asset_fullpath("body_p2.png"))


def get_weapon_img():
    return pygame.image.load(get_asset_fullpath("weapon_p2.png"))
