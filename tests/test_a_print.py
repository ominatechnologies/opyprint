# test_a_print

from io import StringIO

from opyprint import PPContext, print as pprint


def test_print_1():
    string_io = StringIO()
    pprint(file=string_io)
    result = string_io.getvalue()
    # print("\n" + result)
    assert result == "\n"


def test_print_2():
    string_io = StringIO()
    pprint("- key", [4, 5, 6], file=string_io)
    result = string_io.getvalue()
    # print("\n" + result)
    assert result == "- key: [4, 5, 6]\n"


def test_print_3():
    string_io = StringIO()
    PPContext.print_name_value_pairs = False
    pprint([4, 5, 6], file=string_io)
    result = string_io.getvalue()
    # print("\n" + result)
    assert result == "[4, 5, 6]\n"
    PPContext.print_name_value_pairs = True


def test_print_4():
    string_io = StringIO()
    pprint("- key", "12345 67890 12345 67890 12345 67890",
           width=20, file=string_io)
    result = string_io.getvalue()
    # print("\n" + result)
    assert result == """- key: 12345 67890
  12345 67890 12345
  67890
"""


def test_print_5_example():
    string_io = StringIO()
    pprint({'alpha': [1, 2, 3], 'beta': "satisfied"},
           end="\n[END]", file=string_io)
    result = string_io.getvalue()
    # print("\n" + result)
    assert result == """- alpha: [1, 2, 3]
- beta: satisfied
[END]"""
