# test_e_describe

from wpyprint import PPContext


class Alpha:
    @staticmethod
    def describe(ppc: PPContext = None):
        ppc = ppc or PPContext()
        ppc("AL_1")
        ppc("AL_2")
        with ppc.bullets():
            ppc("B1")
            ppc("B2")
        with ppc.indent():
            ppc("I1")
            with ppc.bullets():
                ppc("I2")
        ppc("L3")
        return ppc.flush()


def test_describe_alpha_1():
    ppc = PPContext()
    ppc("L1")
    ppc("foobar", Alpha(), bullet="#")
    ppc("L4")
    result = ppc.flush()
    # print("\n" + result)
    assert result == """L1
# foobar: AL_1
    AL_2
    - B1
    - B2
      I1
      - I2
    L3
L4"""


def test_describe_alpha_2():
    ppc = PPContext()
    ppc("L1")
    ppc("foobar", Alpha())
    ppc("L4")
    result = ppc.flush()
    # print(f"- result: {result}")
    assert result == """L1
foobar: AL_1
  AL_2
  - B1
  - B2
    I1
    - I2
  L3
L4"""


class Beta:
    @staticmethod
    def describe(ppc: PPContext = None):
        ppc = ppc or PPContext()
        ppc("1234567890")
        with ppc.indent():
            ppc("1234567890")
            ppc("1234567890")
        return ppc.flush()

    def __str__(self):
        return f"<{self.describe()}>"


def test_describe_beta_1():
    ppc = PPContext(width=100)
    pair = (Beta(), Beta())
    result = ppc.format((pair, pair))
    # print("\n" + result)
    assert result == """- - 1234567890
      1234567890
      1234567890
  - 1234567890
      1234567890
      1234567890
- - 1234567890
      1234567890
      1234567890
  - 1234567890
      1234567890
      1234567890"""

# def test_describe_beta_2():
#     ppc = PPContext(width=20)
#     pair = (f"{Beta()}", f"{Beta()}")
#     result = ppc.format((pair, pair))
#     # print("\n" + result)
