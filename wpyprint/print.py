from __future__ import annotations

from .PPContext import PPContext

_py_print = print


def print(*args,
          bullet: str = None,
          width: int = PPContext.default_width,
          **kwargs) -> None:
    """
    A drop-in replacement for the standard Python print function that
    pretty-prints the given arguments.

    >>> from wpyprint import print
    >>> print({'alpha': [1, 2, 3], 'beta': "satisfied"})
    - alpha: [1, 2, 3]
    - beta: satisfied

    :param args: When called with two argument and the
        :attr:`wpyprint.PPContext.print_name_value_pairs` attribute is true,
        then the arguments are printed as a name-value pair (in a dict).
        Otherwise multiple arguments are printed as list.
    :param bullet: When given, prefix the formatted result with a bullet,
        when this is not yet the case. The argument may be either a
        non-empty string, the first character of which is taken
        as the bullet, or true to use the current or default bullet.
    :param width: Total width in characters, including bullets and
        indentation. Defaults to the value of the 'default_width' class
        attribute of the :class:`~wpyprint.PPContext.PPContext` class.
    """
    PPContext(width=width).print(*args, bullet=bullet, **kwargs)
