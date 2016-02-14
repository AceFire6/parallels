import pygame
from pygame import Color

from lib.vec2d import Vec2d


class UI(object):
    def __init__(self):
        self.elements = []

    def add_element(self, element):
        self.elements.append(element)

    def get_element(self, element_name):
        for element in self.elements:
            if element_name == element.name:
                return element

    def hide_element(self, element_name):
        self.get_element(element_name).hide()

    def show_element(self, element_name):
        self.get_element(element_name).show()


class UIElement(object):
    def __init__(self, text, x, y, size, name, colour=Color('WHITE')):
        self.x = x
        self.y = y
        self.name = name
        self.text = text
        self.colour = colour
        self._font = pygame.font.SysFont(None, size)
        self.rendered_text = self._font.render(text, 0, colour)
        self.hidden = False

    @property
    def pos(self):
        return self.x, self.y

    def set_position(self, x_or_pair, y=None):
        if y is not None:
            self.x = x_or_pair
            self.y = y
        else:
            self.x = x_or_pair.x
            self.y = x_or_pair.y

    def get_width(self):
        return self.rendered_text.get_width()

    def get_height(self):
        return self.rendered_text.get_height()

    def hide(self):
        self.hidden = True

    def show(self):
        self.hidden = False

    def render_text(self):
        self.rendered_text = self._font.render(self.text, 0, self.colour)

    def update_text(self, new_text):
        self.text = new_text
        self.render_text()
