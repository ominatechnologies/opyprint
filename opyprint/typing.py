from __future__ import annotations

from typing import Any, Collection, Union

from .pp_styles import PPStyles

StyleOptions = Union[PPStyles, str, int,
                     Collection[Union[PPStyles, str, int,
                                      Collection[Any]]]]
"""
Either a single style option or a collection of style options, each of which
can be one of the following:

- One of the keys in the 'ansi_codes' mapping in the 'apply_style' module.
- A string with an arbitrary ANSI-code combination such as '32' (red), '32;3'
  (italic red), etc.
- An integer in the [0-255] range that identifies one of the colors in the
  extended color set shown in: http://www.lihaoyi.com/post/Ansi/Rainbow256.png
"""
