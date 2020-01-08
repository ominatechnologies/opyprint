# test_f_print

import sys
from io import StringIO

from wpyprint import PPContext, print as pprint


def test_ppc_print_1():
    sys.stdout = StringIO()
    ppc = PPContext(width=14)
    ppc([1, 2, 3])
    ppc("key", [4, 5])
    ppc(1234567, 2, 3)
    ppc.print()
    result = sys.stdout.getvalue()
    sys.stdout = sys.__stdout__
    # print("\n" + result)
    assert result == """[1, 2, 3]
key: [4, 5]
- 1234567
- 2
- 3
"""
    assert ppc.flush() == ""


def test_ppc_print_2():
    sys.stdout = StringIO()
    PPContext.print_name_value_pairs = False
    ppc = PPContext(width=12)
    assert not ppc.print_name_value_pairs
    ppc([1, 2, 3])
    ppc("key", [4, 5, 6])
    ppc.print()
    result = sys.stdout.getvalue()
    sys.stdout = sys.__stdout__
    # print("\n" + result)
    assert result == """[1, 2, 3]
- key
- [4, 5, 6]
"""
    assert ppc.flush() == ""
    PPContext.print_name_value_pairs = True
