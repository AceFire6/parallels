import pygame
from pygame.color import Color

from lib.vec2d import Vec2d

from game import Game
from grid import Grid, DrawnLine
from main_menu import MainMenu
from level_manager import LevelManager


MAIN_MENU = None
FINISHED = False
MOVES = 0
RESETS = 0
START_TIME = 0

LINES = []
CUR_LINE = None
GRID_SIZE = 0  # 100  # 100 x 100 grid
GRID = None

# Colours
WHITE = Color('White')
BLACK = Color('Black')
RED = Color('Red')
GREEN = Color('Green')
BLUE = Color('Blue')

COLOURS = [WHITE, RED, GREEN, BLUE]


def setup():
    global GRID, GRID_SIZE

    num_blocks = 5
    screen = pygame.display.get_surface()
    GRID_SIZE = screen.get_width() / num_blocks
    GRID = Grid(num_blocks, num_blocks, GRID_SIZE)  # Cols, Rows

    GRID.add_ui(Game())

    level_manager = LevelManager()
    level_manager.setup_levels()
    GRID.add_level_manager(level_manager)


def reset_game():
    global CUR_LINE, FINISHED, START_TIME, MOVES, RESETS

    if CUR_LINE:
        CUR_LINE.start_terminal.set_used(False)
    GRID.reset()
    CUR_LINE = None
    FINISHED = False
    GRID.ui.reset()
    MOVES += 1
    RESETS += 1
    # START_TIME = pygame.time.get_ticks()


def go_to_main_menu():
    reset_game()
    GRID.ui.stop()
    MAIN_MENU.show()


def events():
    """Event section of game loop. Handle user input. Return boolean."""
    global CUR_LINE, FINISHED, MOVES, START_TIME

    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # Program window quit button press
            return False
        elif event.type == pygame.KEYUP:  # Key pressed event
            if not MAIN_MENU.hidden:
                return MAIN_MENU.handle_keypress(event.key)

            if event.key == pygame.K_ESCAPE:
                go_to_main_menu()
            elif event.key == pygame.K_r:
                reset_game()
            elif event.key == pygame.K_RETURN and GRID.is_completed:
                if not GRID.level_manager.next_level():
                    go_to_main_menu()
                    GRID.terminals = {}
                else:
                    GRID.level_manager.write_to_file(
                            MOVES, RESETS, GRID.ui.time)
                    reset_game()
                    MOVES = 0
        elif event.type == pygame.MOUSEBUTTONDOWN and not FINISHED:  # Mouse
            states = pygame.mouse.get_pressed()
            mouse_pos = Vec2d(pygame.mouse.get_pos())
            if states == (1, 0, 0):  # Left click
                if not MAIN_MENU.hidden:
                    if not MAIN_MENU.handle_click(mouse_pos):
                        return False

                terminal = GRID.get_terminal(mouse_pos)
                if not CUR_LINE:
                    x, y = mouse_pos
                    if terminal:  # and not terminal.used:
                        MOVES += 1
                        CUR_LINE = DrawnLine(GRID, x, y, terminal.colour)
                        if terminal.used:
                            GRID.edit_line(terminal.group)
                        terminal.set_used()
                else:
                    click_point = GRID.get_vec_grid_coords(mouse_pos)
                    adj_blocks = CUR_LINE.get_grid_possible_moves()
                    if click_point in adj_blocks:
                        MOVES += 1
                        if terminal and not terminal.used:  # line is finished
                            if terminal.group == CUR_LINE.group:
                                CUR_LINE.add_point(mouse_pos)
                                CUR_LINE.set_end_terminal()
                                terminal.set_used()
                                GRID.add_line(CUR_LINE)
                                CUR_LINE = None
                        else:
                            CUR_LINE.add_point(mouse_pos)
            elif states == (0, 0, 1):  # Right click
                if CUR_LINE:
                    CUR_LINE.start_terminal.set_used(False)
                    CUR_LINE = False

    return True


def update():
    global FINISHED

    GRID.ui.get_element('move_count').update_text('Moves: %d' % MOVES)

    if GRID.is_completed:
        FINISHED = True
        GRID.ui.show_element('win_text')
    else:
        if GRID.ui.running and MAIN_MENU.hidden:
            GRID.ui.update()
        elif MAIN_MENU.hidden and not GRID.ui.running:
            GRID.ui.start()


def render():
    """Render section of game loop. Handle drawing."""
    if not MAIN_MENU.hidden:
        MAIN_MENU.render()
    else:
        GRID.ui.render(GRID, CUR_LINE)

    pygame.display.flip()


def main():
    """Main game loop. Loop until events returns false."""
    global START_TIME, MAIN_MENU

    pygame.init()
    pygame.display.set_caption('Path Finder')
    pygame.display.set_mode((600, 650), pygame.SRCALPHA)

    MAIN_MENU = MainMenu()

    running = True

    setup()

    clock = pygame.time.Clock()
    START_TIME = pygame.time.get_ticks()
    while running:
        clock.tick(60)
        pygame.time.wait(1)
        running = events()
        update()
        render()
    pygame.quit()


if __name__ == "__main__":
    main()
