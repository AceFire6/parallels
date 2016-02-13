import pygame
from pygame import Rect
from pygame.color import Color

from lib.vec2d import Vec2d

from grid import Grid, DrawnLine
from utils import alpha, get_inner_square, get_inner_square_from_point

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
    GRID.add_terminals('4', Vec2d(0, 2), Vec2d(1, 4), RED + BLUE)


def events():
    """Event section of game loop. Handle user input. Return boolean."""
    global CUR_LINE

    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # Program window quit button press
            return False
        elif event.type == pygame.KEYUP:  # Key pressed event
            if event.key == pygame.K_ESCAPE:
                return False
        elif event.type == pygame.MOUSEBUTTONDOWN:  # Mouse event
            states = pygame.mouse.get_pressed()
            mouse_pos = Vec2d(pygame.mouse.get_pos())
            if states == (1, 0, 0):  # Left click
                terminal = GRID.get_terminal(mouse_pos)
                if not CUR_LINE:
                    if terminal and not terminal.used:
                        x, y = mouse_pos
                        CUR_LINE = DrawnLine(GRID, x, y, terminal.colour)
                        terminal.set_used()
                else:
                    click_point = GRID.get_vec_grid_coords(mouse_pos)
                    adj_blocks = CUR_LINE.get_grid_possible_moves()
                    if click_point in adj_blocks:
                        if terminal and not terminal.used:  # line is finished
                            if terminal.group == CUR_LINE.group:
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
    """Update the formation and units."""
    pass


def render(screen):
    """Render section of game loop. Handle drawing."""
    mouse_pos = Vec2d(pygame.mouse.get_pos())
    m_grid_pos = GRID.get_vec_grid_coords(mouse_pos.x, mouse_pos.y)

    screen.fill(BLACK)
    screen.set_colorkey(BLACK)

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

    pygame.display.flip()


def main():
    """Main game loop. Loop until events returns false."""

    pygame.init()
    pygame.display.set_caption("Parallels")
    screen = pygame.display.set_mode((600, 600), pygame.SRCALPHA)

    running = True

    setup()

    clock = pygame.time.Clock()
    while running:
        clock.tick(60)
        pygame.time.wait(1)
        running = events()
        update()
        render(screen)


if __name__ == "__main__":
    main()
