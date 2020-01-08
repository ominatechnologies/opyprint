# test_b_format

from wpyprint import PPContext


def test_empty_1():
    ppc = PPContext()
    result = ppc.format()
    # print("\n" + result)
    assert result == ""

    result = ppc.format("")
    # print("\n" + result)
    assert result == ""


def test_str_1():
    ppc = PPContext()
    result = ppc.format("foobar")
    # print("\n" + result)
    assert result == "foobar"

    result = ppc.format("foo\nbar")
    # print("\n" + result)
    assert result == "foo\nbar"


def test_str_2():
    ppc = PPContext()
    result = ppc.format("foo\nbar", bullet="+")
    # print("\n" + result)
    assert result == "+ foo\n  bar"

    result = ppc.format("foo\nbar", bullet="+ ")
    # print("\n" + result)
    assert result == "+ foo\n  bar"

    result = ppc.format("foo\nbar", bullet="+++++")
    # print("\n" + result)
    assert result == "+ foo\n  bar"


def test_str_3():
    ppc = PPContext(bullet="+")
    result = ppc.format("foo\nbar")
    # print("\n" + result)
    assert result == "+ foo\n  bar"

    ppc = PPContext(indent="....")
    result = ppc.format("foo\nbar")
    # print("\n" + result)
    assert result == "....foo\n....bar"

    ppc = PPContext(bullet="+", indent="....")
    result = ppc.format("foo\nbar")
    # print("\n" + result)
    assert result == "....+ foo\n....  bar"

    ppc = PPContext(bullet="+")
    result = ppc.format("foo\nbar", bullet="+")
    # print("\n" + result)
    assert result == "+ foo\n  bar"

    ppc = PPContext(bullet="+")
    result = ppc.format("foo\nbar", bullet="✕")
    # print("\n" + result)
    assert result == "✕ foo\n  bar"


def test_str_4_wrap():
    ppc = PPContext(width=10, truncate=3)
    result = ppc.format("w1 w2 w3 w4 w5")
    # print("\n" + result)
    assert result == "w1 w2 w3\nw4 w5"

    result = ppc.format("w1 w2 w3 w4 w55 w66 w77 w88 w99")
    # print("\n" + result)
    assert result == "w1 w2 w3\nw4 w55 w66\nw77 [...]"


def test_list_1():
    val = []
    ppc = PPContext()
    result = ppc.format(val)
    # print("\n" + result)
    assert result == """[]"""

    val = ["abc", "def", "ghi", "jkl"]
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

    ppc = PPContext(width=16, bullet="+")
    result = ppc.format(val)
    # print("\n" + result)
    assert result == """+ - abc
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


def test_generator_1():
    ppc = PPContext()
    result = ppc.format((i for i in [1, 2, 3, 4, 5]))
    # print("\n" + result)
    assert result == "[1, 2, 3, 4, 5]"

    ppc = PPContext(truncate=2)
    result = ppc.format((i for i in [1, 2, 3, 4, 5]))
    # print("\n" + result)
    assert result == "[1, 2, ...]"


def test_set_1():
    ppc = PPContext()

    result = ppc.format({1, 2, 3, 4, 5})
    # print("\n" + result)
    assert result == "{1, 2, 3, 4, 5}"

    result = ppc.format({3, 1, 5, 4, 3, 2})
    # print("\n" + result)
    assert result == "{1, 2, 3, 4, 5}"


def test_set_2_truncated():
    ppc = PPContext(truncate=2)

    result = ppc.format({1, 2, 3, 4, 5})
    # print("\n" + result)
    assert result == "{1, 2, ...}"

    result = ppc.format({3, 1, 5, 4, 3, 2})
    # print("\n" + result)
    assert result == "{1, 2, ...}"


def test_dict_1():
    ppc = PPContext()
    result = ppc.format({})
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

    result = ppc.format(val, bullet="✕")
    # print("\n" + result)
    assert result == """✕ abc: 123
✕ def: 456
✕ ghi: 789"""


def test_dict_3():
    ppc = PPContext(width=16)
    result = ppc.format({'abc': 123, 'def': 456, 'ghi': 789})
    # print("\n" + result)
    assert result == """- abc: 123
- def: 456
- ghi: 789"""

    ppc = PPContext(width=16)
    result = ppc.format({'abcdefghi': 123456789, 'def': 456, 'ghi': 789})
    # print("\n" + result)
    assert result == """- abcdefghi:
    123456789
- def: 456
- ghi: 789"""

    ppc = PPContext(width=16)
    result = ppc.format(
        {'abcdefghijklmnop': 123456789, 'def': 456, 'ghi': 789})
    # print("\n" + result)
    assert result == """- abcdefg...:
    123456789
- def: 456
- ghi: 789"""

    ppc = PPContext(width=18)
    result = ppc.format({
        'abcdefghi': "abc def ghi jkl mno pqr stu",
        'def': 456,
        'ghi': 789,
    })
    # print("\n" + result)
    assert result == """- abcdefghi: abc
    def ghi jkl
    mno pqr stu
- def: 456
- ghi: 789"""


def test_dict_4():
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
