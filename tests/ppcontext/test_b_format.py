# test_b_format

from wpyprint import PPContext


def test_empty_1():
    ppc = PPContext()
    result = ppc.format()
    # print("\n" + result)
    assert result == ""

    result = ppc.format("")
    # print("\n" + result)
    assert result == ''


def test_str_1():
    ppc = PPContext()
    result = ppc.format("foobar")
    # print("\n" + result)
    assert result == 'foobar'

    result = ppc.format("foo\nbar")
    # print("\n" + result)
    assert result == 'foo\nbar'


def test_list_1():
    val = []
    ppc = PPContext()
    result = ppc.format(val)
    # print("\n" + result)
    assert result == """[]"""

    val = ['abc', 'def', 'ghi', 'jkl']
    ppc = PPContext()
    result = ppc.format(val)
    # print("\n" + result)
    assert result == """[abc, def, ghi, jkl]"""

    ppc = PPContext(width=16)
    result = ppc.format(val)
    # print("\n" + result)
    assert result == """- abc
- def
- ghi
- jkl"""


def test_list_2():
    ppc = PPContext(truncate=2)

    result = ppc.format([1, 2, 3, 4, 5])
    # print("\n" + result)
    assert result == "[1, 2, ...]"

    result = ppc.format((1, 2, 3, 4, 5))
    # print("\n" + result)
    assert result == "(1, 2, ...)"

    result = ppc.format({5, 2, 1, 4, 3})
    # print("\n" + result)
    assert result == "{1, 2, ...}"

    result = ppc.format((i for i in [1, 2, 3, 4, 5]))
    # print("\n" + result)
    assert result == "[1, 2, ...]"

    result = ppc.format({"d": 4, "b": 2, "c": 3, "a": 1})
    # print("\n" + result)
    assert result == """- a: 1
- b: 2
- ..."""


def test_list_3():
    ppc = PPContext(width=15)
    str_1 = "1234567890\n1234567890"
    str_2 = "1234567890\n1234567890"
    result = ppc.format((str_1, str_2))
    # print("\n" + result)
    assert result == """- 1234567890
  1234567890
- 1234567890
  1234567890"""


def test_dict_1():
    val = {}
    ppc = PPContext()
    result = ppc.format(val)
    # print("\n" + result)
    assert result == """{}"""


def test_dict_2():
    val = {'abc': 123, 'def': 456, 'ghi': 789}
    ppc = PPContext()
    result = ppc.format(val)
    # print("\n" + result)
    assert result == """- abc: 123
- def: 456
- ghi: 789"""


def test_dict_3():
    val = {'abc': 123, 'def': 456, 'ghi': 789}
    ppc = PPContext(width=16)
    result = ppc.format(val)
    # print("\n" + result)
    assert result == """- abc: 123
- def: 456
- ghi: 789"""


def test_dict_4():
    val = {'abcdefghi': 123456789, 'def': 456, 'ghi': 789}
    ppc = PPContext(width=16)
    result = ppc.format(val)
    # print("\n" + result)
    assert result == """- abcdefghi:
    123456789
- def: 456
- ghi: 789"""


def test_dict_5():
    val = {
        'abcdefghi': "abc def ghi jkl mno pqr stu",
        'def': 456,
        'ghi': 789,
    }
    ppc = PPContext(width=18)
    result = ppc.format(val)
    # print("\n" + result)
    assert result == """- abcdefghi: abc
    def ghi jkl
    mno pqr stu
- def: 456
- ghi: 789"""


def test_dict_6():
    val = {'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': 5, 'f': 6, 'g': 7, 'h': 8}
    ppc = PPContext(truncate=4)
    result = ppc.format(val)
    # print("\n" + result)
    assert result == """- a: 1
- b: 2
- c: 3
- d: 4
- ..."""


def test_composite_1():
    val = [
        {'abc': 123, 'def': 456},
        {'ghi': 789}
    ]
    ppc = PPContext()
    result = ppc.format(val)
    # print("\n" + result)
    assert result == """- - abc: 123
  - def: 456
- ghi: 789"""


def test_composite_2():
    val = {
        'abc': [123, 456],
        'abcdefghi': "abc def ghi jkl mno pqr stu",
        'ghi': {'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': 5, 'f': 6, 'g': 7},
    }
    ppc = PPContext(width=18, truncate=4)
    result = ppc.format(val)
    # print("\n" + result)
    assert result == """- abc: [123, 456]
- abcdefghi: abc
    def ghi jkl
    mno pqr stu
- ghi:
    - a: 1
    - b: 2
    - c: 3
    - d: 4
    - ..."""


def test_composite_3():
    val = {
        'abc': (v for v in [1, 2, 3]),
    }
    ppc = PPContext(width=16, truncate=4)
    result = ppc.format(val)
    # print("\n" + result)
    assert result == """abc: [1, 2, 3]"""

# def test_bullet_1():
#     ppc = PPContext()
#     result = ppc.format(val)
#     # print("\n" + result)
#     assert result == """abc: [1, 2, 3]"""
