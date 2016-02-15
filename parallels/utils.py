from pygame import Rect

from lib.vec2d import Vec2d


def get_inner_square(square):
    inner_sq = Rect(square)
    inner_sq.x += 4
    inner_sq.y += 4
    inner_sq.width -= 7
    inner_sq.height -= 7

    return inner_sq


def get_inner_square_from_point(vec_point, size):
    square = Rect(vec_point.x * size, vec_point.y * size, size, size)
    return get_inner_square(square)


def alpha(color, alpha_val):
    color.a = alpha_val
    return color


def center_text(text, x, y, width, height):
    center = Vec2d(x + width, y + height) / 2
    text_adjustment = Vec2d(-text.get_width() / 2, -text.get_height() / 2)
    return center + text_adjustment


def center_element_x(element, width):
    center = (Vec2d(element.pos) + Vec2d(width, 0)) / 2
    text_adjustment = Vec2d(-element.get_width() / 2, 0)
    return center + text_adjustment
