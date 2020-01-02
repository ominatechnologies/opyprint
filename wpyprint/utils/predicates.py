from frozendict import frozendict


def is_dict(obj) -> bool:
    """Checks if the given object is either a dict or a frozendict."""
    return isinstance(obj, dict) or isinstance(obj, frozendict)


def is_set(obj) -> bool:
    """Checks if the given object is either a set or a frozenset."""
    return isinstance(obj, set) or isinstance(obj, frozenset)


def is_multiline(txt) -> bool:
    """Checks if the given string contains newlines."""
    return len(txt.splitlines()) > 1


def is_singleline(txt) -> bool:
    """Checks if the given string contains no newlines."""
    return len(txt.splitlines()) == 1
