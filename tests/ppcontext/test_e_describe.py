# test_e_describe

from wpyprint import PPContext


def test_describe_1():
    ppc = PPContext()
    ppc("L1")
    ppc("foobar", Foobar(), bullet="#")
    ppc("L4")
    result = ppc.flush()
    # print("\n" + result)
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
- foobar: L2
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
        with ppc.bullets():
            ppc("B1")
            ppc("B2")
        with ppc.indent():
            ppc("I1")
            with ppc.bullets():
                ppc("I2")
        ppc("L3")
        return ppc.flush()
