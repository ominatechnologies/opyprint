from __future__ import annotations

from enum import Enum, unique


@unique
class PPStyles(str, Enum):
    # styles:
    blink = 'blink'
    blink_end = 'blink_end'
    bold = 'bold'
    default = 'default'
    dim = 'dim'
    invert = 'invert'
    inverse = 'invert'
    invert_end = 'invert_end'
    inverse_end = 'invert_end'
    italic = 'italic'
    normal = 'normal'
    strike = 'strike'
    strike_end = 'strike_end'
    underline = 'underline'

    # text/fg colors:
    black = 'black'
    blue = 'blue'
    cyan = 'cyan'
    green = 'green'
    magenta = 'magenta'
    red = 'red'
    white = 'white'
    yellow = 'yellow'

    # bold text/fg colors:
    b_black = 'b_black'
    b_blue = 'b_blue'
    b_cyan = 'b_cyan'
    b_green = 'b_green'
    b_magenta = 'b_magenta'
    b_red = 'b_red'
    b_white = 'b_white'
    b_yellow = 'b_yellow'

    # background colors:
    bg_black = 'bg_black'
    bg_blue = 'bg_blue'
    bg_cyan = 'bg_cyan'
    bg_green = 'bg_green'
    bg_magenta = 'bg_magenta'
    bg_red = 'bg_red'
    bg_white = 'bg_white'
    bg_yellow = 'bg_yellow'

    # bold background colors:
    bg_b_black = 'bg_b_black'
    bg_b_blue = 'bg_b_blue'
    bg_b_cyan = 'bg_b_cyan'
    bg_b_green = 'bg_b_green'
    bg_b_magenta = 'bg_b_magenta'
    bg_b_red = 'bg_b_red'
    bg_b_white = 'bg_b_white'
    bg_b_yellow = 'bg_b_yellow'

    # extended colors:
    grey = 'grey'
    grey_0 = 'grey_0'
    grey_1 = 'grey_1'
    grey_2 = 'grey_2'
    grey_3 = 'grey_3'
    grey_4 = 'grey_4'
    grey_5 = 'grey_5'

    # bold extended colors:
    b_grey = 'b_grey'
    b_grey_0 = 'b_grey_0'
    b_grey_1 = 'b_grey_1'
    b_grey_2 = 'b_grey_2'
    b_grey_3 = 'b_grey_3'
    b_grey_4 = 'b_grey_4'
    b_grey_5 = 'b_grey_5'
