import pygame
from pygame import Color, Rect

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
    def __init__(self, x, y, name):
        self.x = x
        self.y = y
        self.name = name
        self.hidden = False

    def hide(self):
        self.hidden = True

    def show(self):
        self.hidden = False

    @property
    def pos(self):
        return Vec2d(self.x, self.y)

    def set_position(self, x_or_pair, y=None):
        if y is not None:
            self.x = x_or_pair
            self.y = y
        else:
            self.x, self.y = x_or_pair


class UIGroup(UIElement):
    def __init__(self, x, y, name):
        super(UIGroup, self).__init__(x, y, name)
        self.elements = []

    def add_element(self, element):
        element.set_position(Vec2d(element.pos) + Vec2d(self.pos))
        self.elements.append(element)

    def get_element_by_pos(self, mouse_pos):
        for element in self.elements:
            if type(element) == UIGroup:
                result = element.get_element_by_pos(mouse_pos)
                if result is not None:
                    return result
            else:
                element_rect = element.rendered_text.get_rect()
                element_rect.move_ip(element.pos.x, element.pos.y)
                if element_rect.collidepoint(mouse_pos):
                    return element

    def get_element_by_name(self, element_name):
        for element in self.elements:
            if element_name == element.name:
                return element

    def set_position(self, x_or_pair, y=None):
        diff = Vec2d(self.pos)
        super(UIGroup, self).set_position(x_or_pair, y)
        diff = Vec2d(self.pos) - diff

        for element in self.elements:
            element.set_position(Vec2d(element.pos) + diff)


class UIText(UIElement):
    def __init__(self, text, x, y, name, size, colour=Color('WHITE')):
        super(UIText, self).__init__(x, y, name)
        self.text = text
        self.colour = colour
        self._font = pygame.font.SysFont(None, size)
        self.rendered_text = self._font.render(text, 0, colour)

    def get_width(self):
        return self.rendered_text.get_width()

    def get_height(self):
        return self.rendered_text.get_height()

    def render_text(self):
        self.rendered_text = self._font.render(self.text, 0, self.colour)

    def update_text(self, new_text):
        self.text = new_text
        self.render_text()
