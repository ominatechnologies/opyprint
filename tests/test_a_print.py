# test_a_print

import sys
from io import StringIO

from opyprint import PPContext, print as pprint


def test_print_1():
    sys.stdout = StringIO()
    pprint()
    result = sys.stdout.getvalue()
    sys.stdout = sys.__stdout__
    # print("\n" + result)
    assert result == "\n"


def test_print_2():
    sys.stdout = StringIO()
    pprint("- key", [4, 5, 6])
    result = sys.stdout.getvalue()
    sys.stdout = sys.__stdout__
    # print("\n" + result)
    assert result == "- key: [4, 5, 6]\n"


def test_print_3():
    sys.stdout = StringIO()
    PPContext.print_name_value_pairs = False
    pprint([4, 5, 6])
    result = sys.stdout.getvalue()
    sys.stdout = sys.__stdout__
    # print("\n" + result)
    assert result == "[4, 5, 6]\n"
    PPContext.print_name_value_pairs = True


def test_print_4():
    sys.stdout = StringIO()
    pprint("- key", "12345 67890 12345 67890 12345 67890", width=20)
    result = sys.stdout.getvalue()
    sys.stdout = sys.__stdout__
    # print("\n" + result)
    assert result == """- key: 12345 67890
  12345 67890 12345
  67890
"""


def test_print_5_example():
    sys.stdout = StringIO()
    pprint({'alpha': [1, 2, 3], 'beta': "satisfied"}, end="\n[END]")
    result = sys.stdout.getvalue()
    sys.stdout = sys.__stdout__
    # print("\n" + result)
    assert result == """- alpha: [1, 2, 3]
- beta: satisfied
[END]"""
