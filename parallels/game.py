import pygame
from pygame import Rect, Color
from ui import UI, UIText, UIGroup
from utils import (alpha, center_text, get_inner_square,
                   get_inner_square_from_point)

from lib.vec2d import Vec2d


class Game(UI):
    def __init__(self):
        super(Game, self).__init__()
        self.setup()
        self.start_time = 0  # pygame.time.get_ticks()
        self.running = False
        self.time = None

    def start(self):
        self.start_time = pygame.time.get_ticks()
        self.running = True

    def stop(self):
        self.time = None
        self.running = False

    def reset(self):
        self.start_time = pygame.time.get_ticks()
        self.hide_element('win_text')

    def setup(self):
        red = (255, 0, 0)
        screen = pygame.display.get_surface()
        width = screen.get_width()
        height = screen.get_height()

        win_text = UIText('YOU DID IT!', 0, 0, 'win_text', 120, red)
        center_position = center_text(win_text, 0, 0, width, height)
        win_text.set_position(center_position)
        win_text.hide()

        self.add_element(win_text)

        move_count = UIText('Moves: 0', 10, 615, 'move_count', size=30)
        self.add_element(move_count)

        timer = UIText('Time: 00:00:000', 0, 0, 'time', size=30)
        x = width - timer.get_width() - 10
        timer.set_position(x, 615)
        self.add_element(timer)

    def update(self):
        cur_time = pygame.time.get_ticks() - self.start_time
        minutes = str(cur_time / 60000).zfill(2)
        seconds = str((cur_time % 60000) / 1000).zfill(2)
        milliseconds = str(cur_time % 1000).zfill(3)
        self.time = (minutes, seconds, milliseconds)
        self.get_element('time').update_text('Time: %s:%s:%s' % self.time)

    def render(self, grid, cur_line):
        mouse_pos = Vec2d(pygame.mouse.get_pos())
        m_grid_pos = grid.get_vec_grid_coords(mouse_pos.x, mouse_pos.y)
        screen = pygame.display.get_surface()
        black = Color('Black')
        white = Color('White')

        screen.fill(black)

        # START DRAW grid
        size = grid.block_size
        for y in xrange(grid.rows):
            for x in xrange(grid.columns):
                cur_square = Rect(x * size, y * size, size, size)
                # grid_val = GRID.get_grid_value(x, y)
                # COLOURS[grid_val]  # Change colour based on grid value
                if m_grid_pos.x == x and m_grid_pos.y == y:
                    # Semi-transparent Hover
                    inner_sq = get_inner_square(cur_square)
                    sur = screen.convert_alpha()
                    pygame.draw.rect(sur, alpha(white, 75), inner_sq)
                    screen.blit(sur, (0, 0))
                pygame.draw.rect(screen, white, cur_square, 2)

        grid.level_manager.render_level()

        for line in grid.finished_lines:
            line_label = line.start_terminal.label
            for point in line.draw_points:
                screen.blit(line_label, point)
        # END DRAW GRID

        # DRAW CUR_LINE
        if cur_line:
            points = cur_line.draw_points
            label = cur_line.start_terminal.label

            for point in points:
                screen.blit(label, point)

            sur = screen.convert_alpha()
            for point in cur_line.get_grid_possible_moves():
                # Semi-transparent Hover
                inner_sq = get_inner_square_from_point(Vec2d(point), size)
                pygame.draw.rect(sur, alpha(white, 50), inner_sq)
            screen.blit(sur, (0, 0))
        # END DRAW CUR_LINE

        # DRAW UI
        for element in self.elements:
            if not element.hidden:
                if type(element) == UIGroup:
                    for el in element.elements:
                        screen.blit(el.rendered_text, el.pos)
                else:
                    screen.blit(element.rendered_text, element.pos)
        # END DRAW UI
