from __future__ import annotations

from typing import Sequence

from .typing import StyleOptions
from .utils import is_oneliner

# Codes can be combined, e.g.:
# - "3;33": italic yellow
# - "3;4;33": italic underlined yellow
#
# Some terminals support a 256-color extended color set:
# - ansi pattern: "\033[38;5;{color}m{content}\033[0m"
#
# For more info: https://en.wikipedia.org/wiki/ANSI_escape_code

fg_colors = {
    # text/fg colors:
    "black": "30",
    "blue_l1": "38;5;117",  # iso "34"
    "blue": "38;5;75",
    "blue_d1": "38;5;32",
    "blue_d2": "38;5;25",
    "cyan_l1": "38;5;123",  # iso "36"
    "cyan": "38;5;44",
    "cyan_d1": "38;5;37",
    "cyan_d2": "38;5;30",
    "green_l1": "38;5;119",  # iso "32"
    "green": "38;5;46",
    "green_d1": "38;5;34",
    "green_d2": "38;5;28",
    "magenta_l1": "38;5;207",  # iso "35"
    "magenta": "38;5;201",
    "magenta_d1": "38;5;127",
    "magenta_d2": "38;5;90",
    "pink_l1": "38;5;219",
    "pink": "38;5;213",
    "pink_d1": "38;5;170",
    "pink_d2": "38;5;133",
    "orange_l1": "38;5;214",
    "orange": "38;5;208",
    "orange_d1": "38;5;202",
    "orange_d2": "38;5;130",
    "red_l1": "38;5;210",  # iso "31"
    "red": "38;5;203",
    "red_d1": "38;5;196",
    "red_d2": "38;5;124",
    "yellow_l1": "38;5;229",  # iso "33"
    "yellow": "38;5;227",
    "yellow_d1": "38;5;184",
    "yellow_d2": "38;5;142",
    "white": "37",
    "grey": "38;5;244",
    "grey_0": "38;5;232",  # == black
    "grey_1": "38;5;236",
    "grey_2": "38;5;240",
    "grey_3": "38;5;244",
    "grey_4": "38;5;248",
    "grey_5": "38;5;252",
}

bg_colors = {
    "black": "40",
    "blue": "48;5;20",
    "blue_d1": "48;5;19",
    "blue_d2": "48;5;18",
    "blue_d3": "48;5;17",
    "cyan": "48;5;37",  # iso: "46"
    "cyan_d1": "48;5;30",
    "cyan_d2": "48;5;23",
    "default": "49",
    "green": "48;5;34",  # iso: "42"
    "green_d1": "48;5;28",
    "green_d2": "48;5;22",
    "grey": "48;5;243",
    "grey_d1": "48;5;241",
    "grey_d2": "48;5;239",
    "grey_d3": "48;5;237",
    "grey_d4": "48;5;235",
    "magenta": "48;5;164",
    "magenta_d1": "48;5;127",
    "magenta_d2": "48;5;90",
    "magenta_d3": "48;5;53",
    "orange": "48;5;202",
    "orange_d1": "48;5;166",
    "orange_d2": "48;5;130",
    "orange_d3": "48;5;94",
    "red": "48;5;160",  # iso "41"
    "red_d1": "48;5;124",
    "red_d2": "48;5;88",
    "red_d3": "48;5;52",
    "yellow": "48;5;142",  # iso "43"
    "yellow_d1": "48;5;100",
    "yellow_d2": "48;5;58",
    "white": "47",
}

ansi_codes = {
    "reset": "0",
    "bold": "1",
    "dim": "2",
    "italic": "3",
    "underline": "4",
    "blink": "5",
    "inverse": "7",
    "invert": "7",
    "strike": "9",
    "default": "10",
    "normal": "22",  # normal color intensity - neither "bold" nor "dim"
    "blink_end": "25",
    "inverse_end": "27",
    "invert_end": "27",
    "strike_end": "29",

    **fg_colors,
    **{f"b_{color}": f"1;{code}" for color, code in fg_colors.items()},

    **{f"bg_{color}": f"0;38;5;15;{code}"
       for color, code in bg_colors.items()},
    **{f"bg_b_{color}": f"0;1;38;5;15;{code}"
       for color, code in bg_colors.items()},
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
        raise TypeError("Unsupported style.")
    elif isinstance(style, Sequence):
        return ";".join(_ansi_code(item) for item in style)
    else:
        raise TypeError(f"Unsupported style '{style}'.")
