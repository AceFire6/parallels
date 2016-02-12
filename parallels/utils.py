from pygame import Rect


def get_inner_square(square):
    inner_sq = Rect(square)
    inner_sq.x += 4
    inner_sq.y += 4
    inner_sq.width -= 7
    inner_sq.height -= 7

    return inner_sq


def alpha(color, alpha_val):
    color.a = alpha_val
    return color
