from frozendict import frozendict


def is_dict(obj) -> bool:
    """Checks if the given object is either a dict or a frozendict."""
    return isinstance(obj, dict) or isinstance(obj, frozendict)


def is_set(obj) -> bool:
    """Checks if the given object is either a set or a frozenset."""
    return isinstance(obj, set) or isinstance(obj, frozenset)


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
