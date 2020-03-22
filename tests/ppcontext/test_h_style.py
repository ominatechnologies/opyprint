# test_h_style

from opyprint import PPContext


class Foo:
    def __str__(self, ppc: PPContext = None):
        ppc = ppc or PPContext()
        ppc("A Foo with:")
        ppc({'k_1': 'v_1', 'k_2': 'v_2'}, style='yellow')
        return ppc.flush()


def test_ppc_style_1():
    ppc = PPContext()

    # print("#1.1:")
    result = ppc.format("__abc__", style='red')
    # print(f"{result}\n{[result]}")
    assert result == "\x1b[31m__abc__\x1b[0m"
    assert len(result) == 7 + 9

    # print("#1.2:")
    result = ppc.format("__abc__", style='italic')
    # print(f"{result}\n{[result]}")
    assert result == "\x1b[3m__abc__\x1b[0m"

    # print("#1.3:")
    result = ppc.format("__abc__", style=('red', 'italic'))
    # print(f"{result}\n{[result]}")
    assert result == "\x1b[31;3m__abc__\x1b[0m"

    # print("#1.4:")
    result = ppc.format("__abc__", style=('grey', 'italic'))
    # print(f"{result}\n{[result]}")
    assert result == "\x1b[38;5;244;3m__abc__\x1b[0m"


def test_ppc_style_2_misc():
    ppc = PPContext(width=16)

    # print("#2.1:")
    result = ppc.format(123, style=('red', 'italic'))
    # print(f"{result}\n{[result]}")
    assert result == "\x1b[31;3m123\x1b[0m"

    # print("#2.2:")
    result = ppc.format(['abc', 123], style=('red', 'italic'))
    # print(f"{result}\n{[result]}")
    assert result == "\x1b[31;3m[abc, 123]\x1b[0m"

    # print("#2.3:")
    result = ppc.format(['abc', 'def', 'ghi', 'jkl'], style=('red', 'italic'))
    # print(f"{result}\n{[result]}")
    assert result == ("- \x1b[31;3mabc\x1b[0m\n"
                      "- \x1b[31;3mdef\x1b[0m\n"
                      "- \x1b[31;3mghi\x1b[0m\n"
                      "- \x1b[31;3mjkl\x1b[0m")

    # print("#2.4:")
    result = ppc.format(Foo(), style=('red', 'italic'))
    # print(f"{result}\n{[result]}")
    assert result == ("\x1b[31;3mA Foo with:\x1b[0m\n"
                      "\x1b[31;3m- \x1b[33mk_1: v_1\x1b[0m\x1b[0m\n"
                      "\x1b[31;3m- \x1b[33mk_2: v_2\x1b[0m\x1b[0m")


def test_ppc_style_3_dict():
    ppc = PPContext(width=16)

    # print("#3.1 - Case KVP-2:")
    obj = {'ef': 'Lorem ipsum dolor sit', }
    result = ppc.format(obj, style=('red', 'italic'))
    # print(f"{result}\n{[result]}")
    assert result == ("\x1b[31;3mef: Lorem ipsum\x1b[0m\n"
                      "  \x1b[31;3mdolor sit\x1b[0m")

    # print("#3.2 - Case KVP-1, KVP-3, KVP-2:")
    obj = {
        'ab': 'xy',
        'cd': 34,
        'ef': 'Lorem ipsum dolor sit',
    }
    result = ppc.format(obj, style=('red', 'italic'))
    # print(f"{result}\n{[result]}")
    assert result == ("- \x1b[31;3mab: xy\x1b[0m\n"
                      "- \x1b[31;3mcd:\x1b[0m \x1b[31;3m34\x1b[0m\n"
                      "- \x1b[31;3mef: Lorem\x1b[0m\n"
                      "    \x1b[31;3mipsum\x1b[0m\n"
                      "    \x1b[31;3mdolor sit\x1b[0m")

    # print("#3.3 - Case KVP-1, KVP-3, KVP-5:")
    obj = {
        'ab': 'xy',
        'cd': ['abc', 123],
        'ef': ['abc', 'def', 'ghi', 'jkl'],
    }
    result = ppc.format(obj, style=('red', 'italic'))
    # print(f"{result}\n{[result]}")
    assert result == ("- \x1b[31;3mab: xy\x1b[0m\n"
                      "- \x1b[31;3mcd:\x1b[0m \x1b[31;3m[abc, 123]\x1b[0m\n"
                      "- \x1b[31;3mef:\x1b[0m\n"
                      "    - \x1b[31;3mabc\x1b[0m\n"
                      "    - \x1b[31;3mdef\x1b[0m\n"
                      "    - \x1b[31;3mghi\x1b[0m\n"
                      "    - \x1b[31;3mjkl\x1b[0m")

    # print("#3.4 - Case KVP-4:")
    obj = {'ab': Foo()}
    result = ppc.format(obj, style=('red', 'italic'))
    # print(f"{result}\n{[result]}")
    assert result == ("\x1b[31;3mab:\x1b[0m \x1b[31;3mA Foo with:\x1b[0m\n"
                      "\x1b[31;3m  - \x1b[33mk_1: v_1\x1b[0m\x1b[0m\n"
                      "\x1b[31;3m  - \x1b[33mk_2: v_2\x1b[0m\x1b[0m")

    # print("#3.5 - Case KVP-1, KVP-5:")
    obj = {'ab': 'xy', 'cd': Foo()}
    result = ppc.format(obj, style=('red', 'italic'))
    # print(f"{result}\n{[result]}")
    assert result == ("- \x1b[31;3mab: xy\x1b[0m\n"
                      "- \x1b[31;3mcd:\x1b[0m\n"
                      "    \x1b[31;3mA Foo with:\x1b[0m\n"
                      "    \x1b[31;3m- \x1b[33mk_1: v_1\x1b[0m\x1b[0m\n"
                      "    \x1b[31;3m- \x1b[33mk_2: v_2\x1b[0m\x1b[0m")


def test_ppc_style_4_extended_colors():
    # print("#4.1:")
    ppc = PPContext()
    ppc("__abc__", style=('red', 'italic'))
    ppc("__def__", style='grey')
    result = ppc.flush()
    assert result == ("\x1b[31;3m__abc__\x1b[0m\n"
                      "\x1b[38;5;244m__def__\x1b[0m")
