# test_b_call

from wpyprint import PPContext


def test_1():
    sources = frozenset({1, 2, 3})
    ppc = PPContext()
    ppc("Title")
    ppc("abc")
    ppc(123)
    ppc([1, 2, 3])
    ppc("* key", (x for x in sources))
    result = ppc.flush()
    # print(result)
    assert result == """Title
abc
123
[1, 2, 3]
* key: [1, 2, 3]"""
    assert ppc.flush() == ""
