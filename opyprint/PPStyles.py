from __future__ import annotations

from enum import Enum, unique


@unique
class PPStyles(str, Enum):
    # styles:
    blink = 'blink'
    bold = 'bold'
    dim = 'dim'
    inverse = 'inverse'
    italic = 'italic'
    normal = 'normal'
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

    # background colors:
    bg_black = 'bg_black'
    bg_blue = 'bg_blue'
    bg_cyan = 'bg_cyan'
    bg_green = 'bg_green'
    bg_magenta = 'bg_magenta'
    bg_red = 'bg_red'
    bg_white = 'bg_white'
    bg_yellow = 'bg_yellow'

    # extended colors:
    grey = 'grey'
    grey_0 = 'grey_0'
    grey_1 = 'grey_1'
    grey_2 = 'grey_2'
    grey_3 = 'grey_3'
    grey_4 = 'grey_4'
    grey_5 = 'grey_5'
