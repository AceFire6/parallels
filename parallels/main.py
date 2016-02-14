import pygame
from pygame import Rect
from pygame.color import Color

from lib.vec2d import Vec2d

from grid import Grid, DrawnLine
from ui import UI, UIElement
from utils import (alpha, center_text, get_inner_square,
                   get_inner_square_from_point)


FINISHED = False
MOVES = 0
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

    # Add terminals to the grid
    GRID.add_terminals('1', Vec2d(0, 1), Vec2d(3, 3), RED)
    GRID.add_terminals('2', Vec2d(4, 0), Vec2d(1, 3), BLUE)
    GRID.add_terminals('3', Vec2d(0, 0), Vec2d(3, 1), GREEN)
    GRID.add_terminals('4', Vec2d(1, 2), Vec2d(1, 4), RED + BLUE)

    width = screen.get_width()
    height = screen.get_height()

    ui = UI()

    win_text = UIElement('YOU DID IT!', 0, 0, 100, 'win_text', RED)
    center_position = center_text(win_text, 0, 0, width, height)
    win_text.set_position(center_position)
    win_text.hide()

    ui.add_element(win_text)

    move_count = UIElement('Moves: 0', 10, 615, 30, 'move_count')
    ui.add_element(move_count)

    timer = UIElement('Time: 00:00:000', 0, 0, 30, 'time')
    x = width - timer.get_width() - 10
    timer.set_position(x, 615)
    ui.add_element(timer)

    GRID.add_ui(ui)
    # finished_font = pygame.font.SysFont('Arial', 100, bold=True)
    # win_text = 'YOU DID IT!'
    # FINISHED_TEXT = finished_font.render(win_text, 0, RED)


def events():
    """Event section of game loop. Handle user input. Return boolean."""
    global CUR_LINE, FINISHED, MOVES, START_TIME

    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # Program window quit button press
            return False
        elif event.type == pygame.KEYUP:  # Key pressed event
            if event.key == pygame.K_ESCAPE:
                return False
            elif event.key == pygame.K_r:
                if CUR_LINE:
                    CUR_LINE.start_terminal.set_used(False)
                GRID.reset()
                CUR_LINE = None
                FINISHED = False
                GRID.ui.get_element('win_text').hide()
                MOVES = 0
                START_TIME = pygame.time.get_ticks()
        elif event.type == pygame.MOUSEBUTTONDOWN and not FINISHED:  # Mouse
            states = pygame.mouse.get_pressed()
            mouse_pos = Vec2d(pygame.mouse.get_pos())
            if states == (1, 0, 0):  # Left click
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
        cur_time = pygame.time.get_ticks() - START_TIME
        minutes = str(cur_time / 60000).zfill(2)
        seconds = str((cur_time % 60000) / 1000).zfill(2)
        milliseconds = str(cur_time % 1000).zfill(3)
        time = (minutes, seconds, milliseconds)
        GRID.ui.get_element('time').update_text('Time: %s:%s:%s' % time)


def render(screen):
    """Render section of game loop. Handle drawing."""
    mouse_pos = Vec2d(pygame.mouse.get_pos())
    m_grid_pos = GRID.get_vec_grid_coords(mouse_pos.x, mouse_pos.y)

    screen.fill(BLACK)

    # START DRAW GRID
    for y in xrange(GRID.rows):
        for x in xrange(GRID.columns):
            cur_square = Rect(
                    x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE)
            # grid_val = GRID.get_grid_value(x, y)
            # COLOURS[grid_val]  # Change colour based on grid value
            colour = WHITE
            if m_grid_pos.x == x and m_grid_pos.y == y:
                # Semi-transparent Hover
                inner_sq = get_inner_square(cur_square)
                sur = screen.convert_alpha()
                pygame.draw.rect(sur, alpha(WHITE, 75), inner_sq)
                screen.blit(sur, (0, 0))
            pygame.draw.rect(screen, colour, cur_square, 2)

    for terms in GRID.terminals.itervalues():
        for term in terms:
            screen.blit(term.label, term.pos)
            # pygame.draw.circle(screen, term.colour, term.pos, term.radius)

    for line in GRID.finished_lines:
        line_label = line.start_terminal.label
        for point in line.draw_points:
            screen.blit(line_label, point)
    # END DRAW GRID

    # DRAW CUR_LINE
    if CUR_LINE:
        points = CUR_LINE.draw_points
        label = CUR_LINE.start_terminal.label

        for point in points:
            screen.blit(label, point)

        sur = screen.convert_alpha()
        for point in CUR_LINE.get_grid_possible_moves():
            # Semi-transparent Hover
            inner_sq = get_inner_square_from_point(Vec2d(point), GRID_SIZE)
            pygame.draw.rect(sur, alpha(WHITE, 50), inner_sq)
        screen.blit(sur, (0, 0))
    # END DRAW CUR_LINE

    # DRAW UI
    if GRID.ui:
        for element in GRID.ui.elements:
            if not element.hidden:
                screen.blit(element.rendered_text, element.pos)
    # END DRAW UI

    pygame.display.flip()


def main():
    """Main game loop. Loop until events returns false."""
    global START_TIME

    pygame.init()
    pygame.display.set_caption("Parallels")
    screen = pygame.display.set_mode((600, 650), pygame.SRCALPHA)

    running = True

    setup()

    clock = pygame.time.Clock()
    START_TIME = pygame.time.get_ticks()
    while running:
        clock.tick(60)
        pygame.time.wait(1)
        running = events()
        update()
        render(screen)


if __name__ == "__main__":
    main()
