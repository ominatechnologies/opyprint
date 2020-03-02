# test_predicates

from frozendict import frozendict
import numpy as np
from opyprint.utils.predicates import (is_bullettable, is_dict, is_multiliner,
                                       is_oneliner, is_set, is_tuple)


def test_is_dict():
    assert is_dict(dict())
    assert is_dict({'a': 1})
    assert is_dict(frozendict())
    assert is_dict(frozendict({'a': 1}))

    assert not is_dict([1, 2, 3])
    assert not is_dict({1, 2, 3})
    assert not is_dict(tuple())
    assert not is_dict((1, 2, 3))
    assert not is_dict("foobar")
    assert not is_dict(123)


def test_is_set():
    assert is_set(set())
    assert is_set({1, 2, 3})
    assert is_set(frozenset({1, 2, 3}))

    assert not is_set([1, 2, 3])
    assert not is_set(tuple())
    assert not is_set((1, 2, 3))
    assert not is_set({'a': 1})
    assert not is_set(frozendict({'a': 1}))
    assert not is_set("foobar")
    assert not is_set(123)


def test_is_tuple():
    assert is_tuple(tuple())
    assert is_tuple((1, 2, 3))

    assert not is_tuple(set())
    assert not is_tuple({1, 2, 3})
    assert not is_tuple(frozenset({1, 2, 3}))
    assert not is_tuple([1, 2, 3])
    assert not is_tuple({'a': 1})
    assert not is_tuple(frozendict({'a': 1}))
    assert not is_tuple("foobar")
    assert not is_tuple(123)


def test_is_multiliner():
    assert is_multiliner("aa\nbb")
    assert not is_multiliner("abc")


def test_is_oneliner():
    assert is_oneliner("abc")
    assert not is_oneliner("aa\nbb")


def test_is_bullettable():
    bullettables = (
        list(),
        [1, 2, 3],
        (1, 2, 3),
        {1, 2, 3},
        (v for v in [1, 2, 3]),
        range(0, 10),
        dict(),
        {'a': 1},
        frozendict({'a': 1}),
    )
    for obj in bullettables:
        assert is_bullettable(obj)

    not_bullettables = (
        "abc",
        b'\x00\x10',
        bytes(),
        bytes(10),
        bytearray(),
        bytearray(10),
        memoryview(b'abc'),
        123,
        np.array([1, 2, 3]),
        np.array([[1, 2, 3], [4, 5, 6]]),
    )
    for obj in not_bullettables:
        assert not is_bullettable(obj)
