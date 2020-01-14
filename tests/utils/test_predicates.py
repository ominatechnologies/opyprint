# test_predicates

from frozendict import frozendict

from opyprint.utils.predicates import (is_dict, is_multiliner, is_oneliner,
                                       is_set, is_tuple)


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
