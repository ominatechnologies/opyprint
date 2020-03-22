from __future__ import annotations

from typing import Sequence

from .typing import StyleOptions
from .utils import is_oneliner

# ANSI Codes:
# - 0: reset
# - 1: bold
# - 2: dim
# - 4: underline
# - 5: blink
# - 22: normal brightness
# - 30-37: normal fg colors
# - 38: use color from extended set - see below for more details
# - 40-47: normal bg colors
# - 48: use color from extended set - see below for more details
# - 90-97: bright fg colors
# - 100-107: bright bg colors
#
# Codes can be combined, e.g.:
# - "3;33": italic yellow
# - "3;4;33": italic underlined yellow
#
# Some terminals support a 256-color extended color set:
# - ansi pattern: "\033[38;5;{color}m{content}\033[0m"
# - color codes: http://www.lihaoyi.com/post/Ansi/Rainbow256.png
#
ansi_codes = {
    # styles:
    'bold': '1',
    'dim': '2',
    'italic': '3',
    'underline': '4',
    'blink': '5',
    'inverse': '7',
    'normal': '22',
    # text/fg colors:
    'black': '30',
    'red': '31',
    'green': '32',
    'yellow': '33',
    'blue': '34',
    'magenta': '35',
    'cyan': '36',
    'white': '37',
    # background colors:
    'bg_black': '40',
    'bg_red': '41',
    'bg_green': '42',
    'bg_yellow': '43',
    'bg_blue': '44',
    'bg_magenta': '45',
    'bg_cyan': '46',
    'bg_white': '47',
    # extended colors:
    'grey': '38;5;244',
    'grey_0': '38;5;232',  # == black
    'grey_1': '38;5;236',
    'grey_2': '38;5;240',
    'grey_3': '38;5;244',
    'grey_4': '38;5;248',
    'grey_5': '38;5;252',
}

ansi_pattern = "\x1b[{}m{}\x1b[0m"


def apply_style(content: str, style: StyleOptions = None) -> str:
    if style is None:
        return content
    elif is_oneliner(content):
        return ansi_pattern.format(_ansi_code(style), content)
    else:
        return "\n".join(ansi_pattern.format(_ansi_code(style), line)
                         for line in content.splitlines())


def _ansi_code(style: StyleOptions) -> str:
    if isinstance(style, str):
        if style in ansi_codes:
            return ansi_codes[style]
        else:
            return style
    elif isinstance(style, int):
        return f"38;5;{style}"
    elif isinstance(style, (bytes, bytearray)):
        raise TypeError(f"Unsupported style.")
    elif isinstance(style, Sequence):
        return ";".join(_ansi_code(item) for item in style)
    else:
        raise TypeError(f"Unsupported style '{style}'.")
