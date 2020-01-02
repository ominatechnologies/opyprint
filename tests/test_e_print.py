# test_e_print
import sys
from io import StringIO

from wpyprint import PPContext, print as pprint


def test_print_1():
    target = "[1, 2, 3]\nkey: [4, 5]\n- 1234567\n- 2\n- 3\n"
    sys.stdout = StringIO()
    ppc = PPContext(width=12)
    ppc([1, 2, 3])
    ppc("key", [4, 5])
    ppc(1234567, 2, 3)
    ppc.print()
    result = sys.stdout.getvalue()
    sys.stdout = sys.__stdout__
    # print(result)
    assert result == target
    assert ppc.flush() == ""


def test_print_2():
    target = "[1, 2, 3]\n- key\n- [4, 5, 6]\n"
    sys.stdout = StringIO()
    PPContext.print_name_value_pairs = False
    ppc = PPContext(width=12)
    assert not ppc.print_name_value_pairs
    ppc([1, 2, 3])
    ppc("key", [4, 5, 6])
    ppc.print()
    result = sys.stdout.getvalue()
    sys.stdout = sys.__stdout__
    # print(result)
    assert result == target
    assert ppc.flush() == ""
    PPContext.print_name_value_pairs = True


def test_print_3():
    target = "key: [4, 5, 6]\n"
    sys.stdout = StringIO()
    pprint("key", [4, 5, 6])
    result = sys.stdout.getvalue()
    sys.stdout = sys.__stdout__
    # print(result)
    assert result == target


def test_print_4():
    target = "[4, 5, 6]\n"
    sys.stdout = StringIO()
    PPContext.print_name_value_pairs = False
    pprint([4, 5, 6])
    result = sys.stdout.getvalue()
    sys.stdout = sys.__stdout__
    # print(result)
    assert result == target
    PPContext.print_name_value_pairs = True
