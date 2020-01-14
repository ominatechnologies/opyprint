from typing import Dict, Union

from frozendict import frozendict

from .predicates import is_dict


def lt(obj_1, obj_2) -> bool:
    """
    Checks if obj_1 < obj_2.

    Tries to compare the objects normally or when both objects are
    dictionaries, uses the :func:`dict_lt` function (which calls this function
    recursively).
    """
    try:
        return obj_1 < obj_2
    except TypeError as error:
        if is_dict(obj_1) and is_dict(obj_2):
            return dict_lt(obj_1, obj_2)
        raise error


def dict_lt(dct_1: Union[Dict, frozendict],
            dct_2: Union[Dict, frozendict]) -> bool:
    """
    Checks if dct_1 < dct_2.

    First tries to compare the sorted key tuples. When those are equal, tries
    to compare the value tuples (sorted by their keys).
    """
    if not is_dict(dct_1) and not is_dict(dct_2):
        return NotImplemented

    keys_1 = tuple(sorted(dct_1.keys()))
    keys_2 = tuple(sorted(dct_2.keys()))
    if keys_1 != keys_2:
        return lt(keys_1, keys_2)

    values_1 = tuple(dct_1[key] for key in keys_1)
    values_2 = tuple(dct_2[key] for key in keys_2)
    if values_1 != values_2:
        return lt(values_1, values_2)

    return False
