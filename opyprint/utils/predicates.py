from typing import Generator

from frozendict import FrozenDict


def is_dict(obj) -> bool:
    """Checks if the given object is either a dict or a frozendict."""
    return isinstance(obj, (dict, FrozenDict))


def is_set(obj) -> bool:
    """Checks if the given object is either a set or a frozenset."""
    return isinstance(obj, (set, frozenset))


def is_tuple(obj) -> bool:
    """Checks if the given object is a tuple."""
    return isinstance(obj, tuple)


def is_multiliner(txt) -> bool:
    """Checks if the given string contains newlines."""
    assert isinstance(txt, str)
    return len(txt.splitlines()) > 1


def is_oneliner(txt) -> bool:
    """Checks if the given string contains no newlines."""
    assert isinstance(txt, str)
    return len(txt.splitlines()) == 1


BULLETTABLE_TYPES = (
    Generator,
    dict,
    FrozenDict,
    frozenset,
    list,
    range,
    set,
    tuple,
)


def is_bullettable(obj) -> bool:
    """
    Checks if the given object can be pretty-printed as a "bulletted" list
    and supports slicing and appending to afford truncation with an added
    ellipsis.

    :param obj: The object to check.
    """
    return isinstance(obj, BULLETTABLE_TYPES)
