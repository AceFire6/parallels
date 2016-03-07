from pygame import display, Color
from copy import deepcopy

from grid import Terminal
from level_definitions import levels


colours = [Color('Red'), Color('Blue'), Color('Green'),
           Color('Orange'), Color('Yellow')]


class LevelManager(object):
    def __init__(self):
        self._current_level = 0
        self.levels = []  # Starts with the main menu

    @property
    def current_level(self):
        return self.levels[self._current_level]

    @property
    def active_terminals(self):
        return self.current_level.terminals

    @property
    def active_terminal_groups(self):
        return self.current_level.grouped_terminals

    def write_to_file(self, moves, resets, time):
        time = '%s:%s:%s' % time
        file_name = 'path-finder-results.txt'
        with open(file_name, 'a') as score_file:
            score_file.write('Level #%d: %d %d %s\n' %
                             (self._current_level, moves, resets, time))

    def next_level(self):
        if self._current_level + 1 != len(self.levels):
            self._current_level += 1
            return True
        else:
            self._current_level = 0
            return False

    def render_level(self):
        self.levels[self._current_level].render()

    def rotate_terminals(self, terminals):
        rotated_term_set = []
        index = 0
        for terminal_set in terminals:
            index += 1
            rotated_set = []
            for terminal in terminal_set:
                rotated_set.append((4 - terminal[1], terminal[0]))
            rotated_term_set.append(rotated_set)
        return rotated_term_set

    def setup_levels(self):
        for name, terminals in levels.iteritems():
            self.add_level(name, terminals)
            term_copy = deepcopy(terminals)
            for i in xrange(3):
                term_copy = deepcopy(self.rotate_terminals(term_copy))
                self.add_level(name, term_copy)

    def add_level(self, name, terminal_sets):
        level = Level(name)
        index = 0
        for terminal_set in terminal_sets:
            for terminal in terminal_set:
                level.add_new_terminal(terminal, 30, colours[index], str(index))
            index += 1
        self.levels.append(level)

    def set_terminals(self, terminals):
        level = self.current_level
        level.drawn_terminals = []
        for terminal in terminals.itervalues():
            level.add_drawn_terminal(terminal)


class Level(object):
    def __init__(self, name):
        self.terminals = []
        self.drawn_terminals = []
        self.grouped_terminals = {}
        self.name = name

    def add_drawn_terminal(self, terminal_pair):
        term1, term2 = terminal_pair
        self.drawn_terminals.append(term1)
        self.drawn_terminals.append(term2)

    def add_new_terminal(self, x_y_pair, radius, colour, group):
        x, y = x_y_pair
        terminal = Terminal(x, y, radius, colour, group)
        self.terminals.append(terminal)
        if self.grouped_terminals.get(group) is not None:
            self.grouped_terminals[group].append(terminal)
        else:
            self.grouped_terminals[group] = [terminal]

    def render(self):
        screen = display.get_surface()
        for terminal in self.drawn_terminals:
            screen.blit(terminal.label, terminal.pos)
            # pygame.draw.circle(screen, terminal.colour, terminal.pos, terminal.radius)
