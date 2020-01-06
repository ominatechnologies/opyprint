from __future__ import annotations

from .PPContext import PPContext

_py_print = print
_ppc = PPContext()


def print(*args, bullet: str = None) -> None:
    """
    A replacement for the standard Python print function that pretty-prints
    the given arguments.

    A shortcut for::

        PPContext().print(*args)

    :param args: When called with two argument and the
        :attr:`wpyprint.PPContext.print_name_value_pairs` attribute is true,
        then the arguments are printed as a name-value pair (in a dict).
        Otherwise multiple arguments are printed as list.
    :param bullet: When given, prefix the formatted result with a bullet,
        when this is not yet the case. The argument may be either a
        non-empty string, the first character of which is taken
        as the bullet, or true to use the current or default bullet.
    """
    if len(args) == 0:
        _py_print()
    else:
        _py_print(_ppc.format(*args, bullet=bullet))
