# test_a_format

from wpyprint import PPContext


def test_empty_1():
    ppc = PPContext()
    result = ppc.format()
    # print(result)
    assert result == "--"


def test_str_1():
    ppc = PPContext()
    result = ppc.format("")
    # print(result)
    assert result == '""'


def test_list_1():
    val = []
    ppc = PPContext()
    result = ppc.format(val)
    # print(result)
    assert result == """[]"""

    val = ['abc', 'def', 'ghi', 'jkl']
    ppc = PPContext()
    result = ppc.format(val)
    # print(result)
    assert result == """[abc, def, ghi, jkl]"""

    ppc = PPContext(width=16)
    result = ppc.format(val)
    # print(result)
    assert result == """- abc
- def
- ghi
- jkl"""


def test_dict_1():
    val = {}
    ppc = PPContext()
    result = ppc.format(val)
    # print(result)
    assert result == """{}"""

    val = {'abc': 123, 'def': 456, 'ghi': 789}
    ppc = PPContext()
    result = ppc.format(val)
    # print(result)
    assert result == """abc: 123
def: 456
ghi: 789"""

    val = {'abc': 123, 'def': 456, 'ghi': 789}
    ppc = PPContext(width=16)
    result = ppc.format(val)
    # print(result)
    assert result == """abc: 123
def: 456
ghi: 789"""

    val = {'abcdefghi': 123456789, 'def': 456, 'ghi': 789}
    ppc = PPContext(width=16)
    result = ppc.format(val)
    # print(result)
    assert result == """abcdefghi:
  123456789
def: 456
ghi: 789"""

    val = {
        'abcdefghi': "abc def ghi jkl mno pqr stu",
        'def': 456,
        'ghi': 789,
    }
    ppc = PPContext(width=16)
    result = ppc.format(val)
    # print(result)
    assert result == """abcdefghi: abc
  def ghi jkl
  mno pqr stu
def: 456
ghi: 789"""

    val = {'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': 5, 'f': 6, 'g': 7, 'h': 8}
    ppc = PPContext(truncate=4)
    result = ppc.format(val)
    # print(result)
    assert result == """a: 1
b: 2
c: 3
d: 4"""


def test_composite_1():
    val = [
        {'abc': 123, 'def': 456},
        {'ghi': 789}
    ]
    ppc = PPContext()
    result = ppc.format(val)
    # print(result)
    assert result == """- abc: 123
  def: 456
- ghi: 789"""


def test_composite_2():
    val = {
        'abc': [123, 456],
        'abcdefghi': "abc def ghi jkl mno pqr stu",
        'ghi': {'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': 5, 'f': 6, 'g': 7},
    }
    ppc = PPContext(width=16, truncate=4)
    result = ppc.format(val)
    # print(result)
    assert result == """abc: [123, 456]
abcdefghi: abc
  def ghi jkl
  mno pqr stu
ghi:
  a: 1
  b: 2
  c: 3
  d: 4"""


def test_composite_3():
    val = {
        'abc': (v for v in [1, 2, 3]),
    }
    ppc = PPContext(width=16, truncate=4)
    result = ppc.format(val)
    # print(result)
    assert result == """abc: [1, 2, 3]"""
