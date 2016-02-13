from pygame import font

from lib.vec2d import Vec2d


class Grid(object):
    def __init__(self, columns, rows, block_size):
        self.columns = columns
        self.rows = rows
        self.block_size = block_size
        self.grid = [[0 for i in xrange(6)] for j in xrange(6)]
        self._terminals_grid = [[None for i in xrange(6)] for j in xrange(6)]
        self.terminals = {}
        self.finished_lines = []

    def add_terminals(self, name, vec_term1, vec_term2, colour):
        center = self.block_size / 2
        term1_pos = self.get_pos_from_grid_coords(vec_term1) + center
        term2_pos = self.get_pos_from_grid_coords(vec_term2) + center

        term1 = Terminal(term1_pos.x, term1_pos.y, 20, colour, name)
        term2 = Terminal(term2_pos.x, term2_pos.y, 20, colour, name)

        self._terminals_grid[vec_term1.y][vec_term1.x] = term1
        self._terminals_grid[vec_term2.y][vec_term2.x] = term2

        self.terminals[name] = (term1, term2)

    def get_vec_grid_coords(self, screen_x_or_pair, screen_y=None):
        if screen_y is not None:
            row = screen_y / self.block_size
            column = screen_x_or_pair / self.block_size

            return Vec2d(column, row)
        else:
            return Vec2d(screen_x_or_pair / self.block_size)

    def get_grid_value(self, x_pos, y_pos):
        row = y_pos / self.block_size
        column = x_pos / self.block_size
        return self.grid[row][column]

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
        self.finished_lines.append(line)


class Terminal(object):
    def __init__(self, x, y, radius, colour, group):
        self.x = x
        self.y = y
        # for colours
        # self.pos = Vec2d(x, y)
        self.radius = radius
        self.colour = (150, 150, 150)  # only for text colour
        self.group = group
        self._font = font.SysFont('Arial', 40, bold=True)
        self.label = self._font.render(group, 0, self.colour)
        # for text version
        self.pos = Vec2d(x - self.label.get_width() / 2,
                         y - self.label.get_height() / 2)
        self.used = False

    def matches(self, other_terminal):
        return self.group == other_terminal.group

    def set_used(self, not_used=None):
        self.used = True
        if not_used:
            self.used = not_used


class DrawnLine(object):
    def __init__(self, grid, start_x, start_y, colour):
        self.grid = grid
        self.start_point = grid.get_vec_grid_coords(start_x, start_y)
        self.grid_points = [self.start_point]
        self.colour = colour

    @property
    def start_terminal(self):
        screen_coords = self.grid.get_pos_from_grid_coords(self.start_point)
        return self.grid.get_terminal(screen_coords)

    def add_point(self, screen_x_or_pair, screen_y=None):
        # TODO: Add moveback logic
        grid_point = self.grid.get_vec_grid_coords(screen_x_or_pair, screen_y)
        self.grid_points.append(grid_point)

    def get_points_adjacent_to_last_point(self):
        point = self.grid_points[-1]
        adjacent_points = []
        if point.y >= 1:
            adjacent_points.append(Vec2d(point.x, point.y - 1))
        if point.y < self.grid.rows:
            adjacent_points.append(Vec2d(point.x, point.y + 1))

        if point.x >= 1:
            adjacent_points.append(Vec2d(point.x - 1, point.y))
        if point.x < self.grid.columns:
            adjacent_points.append(Vec2d(point.x + 1, point.y))

        return adjacent_points
