# test_c_call

from opyprint import PPContext


def test_1():
    sources = frozenset({1, 2, 3})
    ppc = PPContext()
    ppc("Title")
    ppc("abc")
    ppc(123)
    ppc([1, 2, 3])
    ppc("key", (x for x in sources), bullet="*")
    result = ppc.flush()
    # print("\n" + result)
    assert result == """Title
abc
123
[1, 2, 3]
* key: [1, 2, 3]"""
    assert ppc.flush() == ""


def test_call_with_bullet_1():
    ppc = PPContext(width=10)
    ppc.newline()
    ppc("L1", bullet="*")
    ppc([1, 2], bullet=">")
    ppc([111, 222, 333], bullet="+")
    ppc('foo', 'bar', bullet="#")
    result = ppc.flush()
    # print("\n" + result)
    assert result == """
* L1
> [1, 2]
+ 111
+ 222
+ 333
# foo: bar"""


def test_call_with_bullet_2():
    ppc = PPContext(width=10)
    ppc.newline()
    with ppc.indent():
        ppc([111, [222, 333], 444], bullet="+")
    result = ppc.flush()
    # print("\n" + result)
    assert result == """
  + 111
  + - 222
    - 333
  + 444"""
