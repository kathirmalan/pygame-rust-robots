import pygame
from time import sleep

from pygame.sprite import Sprite

from src.asset import get_player_img, get_direction_img, place_direction_img, get_body_img, get_weapon_img
from src.body import Body
from src.position import Position
from src.robot import Robot
from src.util import get_font_fullpath
from src.weapon import Weapon

WIN_WIDTH = 1000
WIN_HEIGHT = 700

# colours
RED = (255, 0, 0, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
GREY = (128, 128, 128)
ORANGE = (255, 69, 0)
BG_COLOR = (255, 255, 255)


class UIBoard:

    def __init__(self, frame, board, cell_size, score_card):
        self.frame = frame
        self.board = board
        self.cell_size = cell_size
        self.score_card = score_card


def show_startup_board(cells_state, game_board):
    pygame.init()
    pygame.font.init()

    ui_board = create_board(game_board.rows, game_board.cols)
    update_board(cells_state, ui_board)

    return ui_board


def create_board(rows, cols):
    frame, score_card = get_frame()
    cell_size = get_cell_size(rows, cols, WIN_WIDTH)
    board = init_board(rows, cols, frame, cell_size)
    return UIBoard(frame, board, cell_size, score_card)


def get_frame(caption='EPITA Robot'):
    frame = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    pygame.display.set_caption(caption)
    frame.fill(BG_COLOR)
    app_heading = pygame.font.Font(get_font_fullpath("Hanalei-Regular.ttf"), 86)
    score_card = pygame.font.SysFont('Times New Roman', 35)

    title_first = app_heading.render("EPITA", False, GREY)
    title_last = app_heading.render("ROBOT", False, GREY)
    bind_obj_in_frame(frame, title_first, (WIN_WIDTH - 275, 30))
    bind_obj_in_frame(frame, title_last, (WIN_WIDTH - 290, 120))

    team_a = score_card.render("PLAYER 1", False, (209, 34, 34))
    bind_obj_in_frame(frame, team_a, (WIN_WIDTH - 320, 320))

    team_b = score_card.render("PLAYER 2", False, (0, 97, 207))
    bind_obj_in_frame(frame, team_b, (WIN_WIDTH - 320, 400))

    return frame, score_card


def get_cell_size(rows, cols, win_width):
    return (win_width * 60 / 100) // cols


def init_board(rows, cols, frame, cell_size):
    board = [[None] * cols for _ in range(rows)]
    print(board)

    for i in range(rows):
        for j in range(cols):
            board[i][j] = get_cell_rect_plain(i, j, frame, cell_size)
    return board


def get_cell_rect_plain(i, j, frame, cell_size):
    return pygame.draw.rect(frame, BLACK, ((j * cell_size) + 50, (i * cell_size) + 30, cell_size, cell_size), 3)


def get_cell_obstacle(i, j, frame, cell_size):
    return pygame.draw.rect(frame, GREY, ((j * cell_size) + 50, (i * cell_size) + 30, cell_size, cell_size))


def bind_obj_in_frame(frame, img, rect):
    frame.blit(img, rect)


count = 0


def update_board(cells_state, ui_board):
    global count
    rows = len(cells_state)
    cols = len(cells_state[0])

    ui_board.images = Sprite()

    for i in range(rows):
        for j in range(cols):
            cell = cells_state[i][j]
            ui_cell = ui_board.board[i][j]
            if isinstance(cell, Robot):
                if cell.is_active:
                    show_active_robot(cell, ui_board)
                else:
                    show_deactived_robot(cell, ui_board)
            elif isinstance(cell, Body):
                attach_img_on_board_cell(get_body_img(), Position(i, j), ui_board.board, ui_board.frame)
            elif isinstance(cell, Weapon):
                attach_img_on_board_cell(get_weapon_img(), Position(i, j), ui_board.board, ui_board.frame)
            else:
                # del ui_cell
                # attach_img_on_board_cell(get_player_img('blue'), Position(i, j), ui_board.board, ui_board.frame)
                ui_board.board[i][j] = get_cell_rect_plain(i, j, ui_board.frame, ui_board.cell_size)
    pygame.display.flip()
    pygame.display.update()
    count += 1
    sleep(2)


def show_active_robot(robot, ui_board):
    show_player_for_team(robot.team_name, robot.position, robot.face_direction.direction, ui_board.board,
                         ui_board.frame)


def show_deactived_robot(robot, ui_board):
    board = ui_board.board
    frame = ui_board.frame
    cell_size = ui_board.cell_size

    # pdb.set_trace()
    position = robot.position
    i, j = position.i, position.j
    print(f"[Deactivated] i = {i}, j= {j}")

    cell = board[position.i][position.j]
    del cell
    rect = get_cell_obstacle(i, j, frame, cell_size)
    board[i][j] = rect


def show_player_for_team(team_name, position, direction, board, frame):
    ui_cell = board[position.i][position.j]

    robot_img = get_player_img(team_name)

    robot_img_rect = robot_img.get_rect()
    robot_img_rect.center = ui_cell.center
    bind_obj_in_frame(frame, robot_img, robot_img_rect)

    direction_img = get_direction_img(direction, team_name)
    direction_img_rect = direction_img.get_rect()
    place_direction_img(direction_img_rect, ui_cell, direction)
    bind_obj_in_frame(frame, direction_img, direction_img_rect)


def attach_img_on_board_cell(img, position, board, frame):
    cell = board[position.i][position.j]

    rect = img.get_rect()
    rect.center = cell.center
    bind_obj_in_frame(frame, img, rect)


def exit_func():
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
    pygame.quit()


if __name__ == '__main__':
    print('UI Board')
