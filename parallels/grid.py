from pygame import font

from lib.vec2d import Vec2d


class Grid(object):
    def __init__(self, columns, rows, block_size):
        self.columns = columns
        self.rows = rows
        self.block_size = block_size
        self.grid = [[0 for i in xrange(columns)] for j in xrange(rows)]
        self._terminals_grid = [
            [None for i in xrange(columns)] for j in xrange(rows)]
        self.terminals = {}
        self.finished_lines = []
        self.ui = None
        self.level_manager = None

    def add_level_manager(self, level_manager):
        self.level_manager = level_manager
        self.update_terminals()

    def update_terminals(self):
        term_iter = self.level_manager.active_terminal_groups.iteritems()
        for group, terminals in term_iter:
            term1_vec = Vec2d(terminals[0].x, terminals[0].y)
            term2_vec = Vec2d(terminals[1].x, terminals[1].y)
            colour = terminals[0].colour
            self.add_terminals(group, term1_vec, term2_vec, colour)
        self.level_manager.set_terminals(self.terminals)

    def add_ui(self, ui):
        self.ui = ui

    def reset(self):
        for line in self.finished_lines:
            line.start_terminal.set_used(False)
            line.end_terminal.set_used(False)

        self.grid = [
            [0 for i in xrange(self.columns)] for j in xrange(self.rows)]
        self._terminals_grid = [
            [None for i in xrange(self.columns)] for j in xrange(self.rows)]
        # for y in xrange(self.rows):
        #     for x in xrange(self.columns):
        #         term_grid_val = self._terminals_grid[y][x]
        #         if term_grid_val is not None:
        #             self.grid[y][x] = term_grid_val.group
        #         else:
        #             self.grid[y][x] = 0
        self.finished_lines = []
        self.update_terminals()

    @property
    def is_completed(self):
        empty = len(self.terminals) == 0
        return len(self.finished_lines) == len(self.terminals) and not empty

    def edit_line(self, line_group):
        for line in self.finished_lines:
            if line.group == line_group:
                line.start_terminal.set_used(False)
                line.end_terminal.set_used(False)
                self.finished_lines.remove(line)

    def add_terminals(self, name, vec_term1, vec_term2, colour):
        self.grid[vec_term1.y][vec_term1.x] = name
        self.grid[vec_term2.y][vec_term2.x] = name

        center = self.block_size / 2
        term1_pos = self.get_pos_from_grid_coords(vec_term1) + center
        term2_pos = self.get_pos_from_grid_coords(vec_term2) + center

        term1 = Terminal(term1_pos.x, term1_pos.y, 20, colour, name)
        term2 = Terminal(term2_pos.x, term2_pos.y, 20, colour, name)

        self._terminals_grid[vec_term1.y][vec_term1.x] = term1
        self._terminals_grid[vec_term2.y][vec_term2.x] = term2

        self.terminals[name] = (term1, term2)

    def get_vec_grid_coords(self, screen_x_or_pair, screen_y=None):
        coords = None
        if screen_y is not None:
            row = screen_y / self.block_size
            column = screen_x_or_pair / self.block_size
            coords = Vec2d(column, row)
        else:
            coords = Vec2d(screen_x_or_pair / self.block_size)
        return self.clamp_to_grid(coords)

    def clamp_to_grid(self, coordinates):
        if coordinates.x >= self.columns:
            coordinates.x = self.columns - 1
        elif coordinates.x < 0:
            coordinates.x = 0
        if coordinates.y >= self.rows:
            coordinates.y = self.rows - 1
        elif coordinates.x < 0:
            coordinates.x = 0
        return coordinates

    def get_grid_value_from_screen(self, screen_x, screen_y):
        y = screen_y / self.block_size
        x = screen_x / self.block_size
        return self.get_grid_value(x, y)

    def get_grid_value(self, x, y):
        return self.grid[y][x]

    def is_grid_collision(self, vec_point, group):
        grid_val = self.get_grid_value(vec_point.x, vec_point.y)
        if grid_val == 0 or grid_val == group:
            return False
        else:
            return True

    def set_grid_value(self, row, column, value):
        self.grid[row][column] = value

    def get_pos_from_grid_coords(self, x_or_pair, y=None):
        if y is not None:
            return Vec2d(x_or_pair * self.block_size, y * self.block_size)
        else:
            return Vec2d(x_or_pair * self.block_size)

    def get_terminal(self, screen_x_or_pair, screen_y=None):
        coords = self.get_vec_grid_coords(screen_x_or_pair, screen_y)
        return self._terminals_grid[coords.y][coords.x]

    def add_line(self, line):
        for point in line.grid_points:
            self.grid[point.y][point.x] = line.start_terminal.group
        self.finished_lines.append(line)


class Terminal(object):
    def __init__(self, x, y, radius, colour, group):
        self.x = x
        self.y = y
        # for colours
        # self.pos = Vec2d(x, y)
        self.radius = radius
        self._active_colour = (255, 255, 255)
        self._inactive_colour = (150, 150, 150)
        self.colour = self._inactive_colour  # only for text colour
        self.group = group
        self._font = font.SysFont('Arial', 40, bold=True)
        self.label = self._font.render(str(int(group)+1), 0, self.colour)
        # for text version
        self.pos = Vec2d(x - self.label.get_width() / 2,
                         y - self.label.get_height() / 2)
        self.used = False

    def render_label(self, colour):
        self.colour = colour
        self.label = self._font.render(str(int(self.group)+1), 0, self.colour)

    def matches(self, other_terminal):
        return self.group == other_terminal.group

    def set_used(self, used=True):
        self.used = used
        self.render_label(self._active_colour)
        if not used:
            self.render_label(self._inactive_colour)
            self.used = used


class DrawnLine(object):
    def __init__(self, grid, start_x, start_y, colour):
        self.grid = grid
        self.start_point = grid.get_vec_grid_coords(start_x, start_y)
        self.start_terminal = self.get_start_terminal()
        self.end_terminal = None
        self.grid_points = [self.start_point]
        self.draw_points = [self.grid_point_to_draw_point(self.start_point)]
        self.colour = colour
        self.group = self.start_terminal.group

    def get_start_terminal(self):
        screen_coords = self.grid.get_pos_from_grid_coords(self.start_point)
        return self.grid.get_terminal(screen_coords)

    def set_end_terminal(self):
        self.end_terminal = self.grid.get_terminal(self.draw_points[-1])

    def add_point(self, screen_x_or_pair, screen_y=None):
        grid_point = self.grid.get_vec_grid_coords(screen_x_or_pair, screen_y)

        for i in xrange(len(self.grid_points)):
            if grid_point == self.grid_points[i]:
                self.grid_points = self.grid_points[:i+1]
                self.draw_points = self.draw_points[:i+1]
                return

        self.grid_points.append(grid_point)
        self.draw_points.append(self.grid_point_to_draw_point(grid_point))

    def get_grid_possible_moves(self):
        point = self.grid_points[-1]
        potential_moves = []
        if point.y >= 1:
            potential_moves.append(Vec2d(point.x, point.y - 1))
        if point.y + 1 < self.grid.rows:
            potential_moves.append(Vec2d(point.x, point.y + 1))

        if point.x >= 1:
            potential_moves.append(Vec2d(point.x - 1, point.y))
        if point.x + 1 < self.grid.columns:
            potential_moves.append(Vec2d(point.x + 1, point.y))

        adjacent_points = []
        for move in potential_moves:
            if not self.grid.is_grid_collision(move, self.group):
                adjacent_points.append(move)
        return adjacent_points

    def get_screen_possible_moves(self):
        moves = self.get_grid_possible_moves()
        return self.grid_points_to_draw_points(moves)

    def grid_point_to_draw_point(self, point):
        label = self.start_terminal.label
        screen_point = self.grid.get_pos_from_grid_coords(point)
        # Only for labels
        screen_point += self.grid.block_size / 2
        screen_point = (screen_point.x - label.get_width() / 2,
                        screen_point.y - label.get_height() / 2)
        return Vec2d(screen_point)

    def grid_points_to_draw_points(self, points):
        return [self.grid_point_to_draw_point(point)for point in points]
