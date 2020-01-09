# test_e_describe

from wpyprint import PPContext


class Alpha:
    def __init__(self, prop_1, prop_2):
        self.prop_1 = prop_1
        self.prop_2 = prop_2

    def describe(self, ppc: PPContext = None):
        ppc = ppc or PPContext()
        ppc("An Alpha object with:")
        with ppc.bullets():
            ppc("prop_1", self.prop_1)
            ppc("prop_2", self.prop_2)
        return ppc.flush()


def test_alpha_1():
    ppc = PPContext()
    ppc.newline()
    ppc(Alpha(1, 2))
    ppc.newline()
    ppc([Alpha(1, 2), Alpha(2, 3)])
    ppc.newline()
    ppc("foobar", Alpha(3, 4), bullet="#")
    ppc("[END]")
    result = ppc.flush()
    # print("\n" + result)
    assert result == """
An Alpha object with:
- prop_1: 1
- prop_2: 2

- An Alpha object with:
  - prop_1: 1
  - prop_2: 2
- An Alpha object with:
  - prop_1: 2
  - prop_2: 3

# foobar: An Alpha object with:
    - prop_1: 3
    - prop_2: 4
[END]"""


def test_alpha_2():
    ppc = PPContext(width=20)
    ppc.newline()
    ppc(Alpha(1, 2))
    ppc.newline()
    ppc([Alpha(1, 2), Alpha(2, 3)])
    ppc.newline()
    ppc("foobar", Alpha(3, 4), bullet="#")
    ppc("[END]")
    result = ppc.flush()
    # print("\n" + result)
    assert result == """
An Alpha object
with:
- prop_1: 1
- prop_2: 2

- An Alpha object
  with:
  - prop_1: 1
  - prop_2: 2
- An Alpha object
  with:
  - prop_1: 2
  - prop_2: 3

# foobar:
    An Alpha object
    with:
    - prop_1: 3
    - prop_2: 4
[END]"""


def test_alpha_3():
    ppc = PPContext()
    ppc.newline()
    ppc(Alpha(Alpha(1, 2), Alpha(3, 4)))
    ppc("[END]")
    result = ppc.flush()
    # print("\n" + result)
    assert result == """
An Alpha object with:
- prop_1: An Alpha object with:
    - prop_1: 1
    - prop_2: 2
- prop_2: An Alpha object with:
    - prop_1: 3
    - prop_2: 4
[END]"""


def test_alpha_4():
    ppc = PPContext(width=20)
    ppc.newline()
    ppc(Alpha(Alpha(1, 2), Alpha(3, 4)))
    ppc("[END]")
    result = ppc.flush()
    # print("\n" + result)
    assert result == """
An Alpha object
with:
- prop_1:
    An Alpha object
    with:
    - prop_1: 1
    - prop_2: 2
- prop_2:
    An Alpha object
    with:
    - prop_1: 3
    - prop_2: 4
[END]"""
