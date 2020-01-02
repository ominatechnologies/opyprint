# test_ppcontext

from wpyprint import PPContext


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


def test_call_1():
    sources = frozenset({1, 2, 3})
    ppc = PPContext()
    ppc("Title")
    ppc("* key", (x for x in sources))
    result = ppc.flush()
    # print(f"- result: {result}")
    assert result == """Title
* key: [1, 2, 3]"""


def test_describe_1():
    ppc = PPContext()
    ppc("L1")
    with ppc.bullet(bullet="#"):
        ppc("foobar", Foobar())
    ppc("L4")
    result = ppc.flush()
    # print(f"- result: {result}")
    assert result == """L1
# foobar: L2
    - B1
    - B2
      I1
      - I2
    L3
L4"""


def test_describe_2():
    ppc = PPContext()
    ppc("L1")
    ppc("foobar", Foobar())
    ppc("L4")
    result = ppc.flush()
    # print(f"- result: {result}")
    assert result == """L1
foobar: L2
  - B1
  - B2
    I1
    - I2
  L3
L4"""


class Foobar:
    @staticmethod
    def describe(ppc: PPContext = None):
        ppc = ppc or PPContext()
        ppc("L2")
        with ppc.bullet():
            ppc("B1")
            with ppc.bullet():
                ppc("B2")
        with ppc.indent():
            ppc("I1")
            with ppc.bullet():
                ppc("I2")
        ppc("L3")
        return ppc.flush()
