from __future__ import annotations

import sys

from .pp_context import PPContext
from .typing import StyleOptions

_py_print = print


def print(*args,
          bullet: str = None,
          end="\n",
          file=sys.stdout,
          flush=False,
          indent: str = "",
          key_style: StyleOptions = None,
          style: StyleOptions = None,
          truncate: int = PPContext.default_truncate,
          width: int = PPContext.default_width,
          sep=" ",
          **kwargs) -> None:
    """
    A drop-in replacement for the standard Python print function that
    pretty-prints the given arguments.

    >>> from opyprint import print
    >>> print({"alpha": [1, 2, 3], "beta": "satisfied"})
    - alpha: [1, 2, 3]
    - beta: satisfied

    :param args: When called with two argument and the
        :attr:`opyprint.pp_context.print_name_value_pairs` attribute is true,
        then the arguments are printed as a name-value pair (in a dict).
        Otherwise multiple arguments are printed as list.
    :param bullet: When given, prefix the formatted result with a bullet,
        when this is not yet the case. The argument may be either a
        non-empty string, the first character of which is taken
        as the bullet, or true to use the current or default bullet.
    :param end: See native 'print' function.
    :param file: See native 'print' function.
    :param flush: See native 'print' function.
    :param indent: The indentation prefix string.
    :param key_style: Optional style specifications for the key part of
        key-value pairs.
    :param sep: See native 'print' function.
    :param style: Optional style specifications.
    :param truncate: The truncation setting. When this value is 0, no
        truncation is applied. When any other positive integer value *n* is
        given, then no more than *n* list/tuple/set elements or dictionary
        items will be included and no more than *n* lines of a wrapped
        string will be included. Defaults to the value of the
        :attr:`PPContext.default_truncate` class attribute.
    :param width: Total width in characters, including bullets and
        indentation. Defaults to the value of the 'default_width' class
        attribute of the :class:`~opyprint.pp_context.PPContext` class.
    """
    PPContext(indent=indent,
              width=width,
              truncate=truncate).print(*args,
                                       bullet=bullet,
                                       end=end,
                                       file=file,
                                       flush=flush,
                                       key_style=key_style,
                                       sep=sep,
                                       style=style,
                                       **kwargs)
