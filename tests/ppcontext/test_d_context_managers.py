# test_d_context_managers

from wpyprint import PPContext


def test_indent():
    ppc = PPContext()
    ppc("L1")
    assert ppc.indentation == ""
    with ppc.indent():
        ppc("B1")
        ppc("B2")
        assert ppc.indentation == "  "
        with ppc.indent():
            ppc("B3")
            ppc("B4")
            with ppc.bullets():
                ppc("B5")
                ppc("B6")
    with ppc.bullets(">>>"):
        ppc("B7")
        ppc("B8")
    result = ppc.flush()
    # print("\n" + result)
    assert result == """L1
  B1
  B2
    B3
    B4
    - B5
    - B6
> B7
> B8"""


def test_bullets_1():
    ppc = PPContext()
    ppc("L1")
    with ppc.bullets():
        ppc("B1")
        ppc("B2")
    with ppc.bullets("*"):
        ppc("B3")
        ppc("B4")
        with ppc.bullets():
            ppc("B5")
            ppc("B6")
            with ppc.bullets('+'):
                ppc("B7a")
                ppc("B7b")
    with ppc.bullets(">>>"):
        ppc("B8")
        ppc("B9")
    result = ppc.flush()
    # print("\n" + result)
    assert result == """L1
- B1
- B2
* B3
* B4
  * B5
  * B6
    + B7a
    + B7b
> B8
> B9"""


def test_bullets_2():
    ppc = PPContext(width=15)
    ppc.newline()
    with ppc.bullets("*"):
        ppc("B1")
        ppc([1, 2, 3])
        ppc.newline()
        ppc([111, 222, 333])
        with ppc.bullets(">"):
            ppc([1, 2, 3])
            ppc([111, 222, 333])
    result = ppc.flush()
    # print("'" + result + "'")
    assert result == """
* B1
* [1, 2, 3]

* - 111
  - 222
  - 333
  > [1, 2, 3]
  > - 111
    - 222
    - 333"""


def test_width():
    txt = "a b c d e f g h i j k l m n o"
    txt2 = "12 3 4 5 6 7 8 9 0 1 2 3 4 5"
    ppc = PPContext(width=20)
    ppc("\n12345678901234567890")
    ppc(txt)
    ppc(txt2)
    ppc('foobar', txt)
    ppc('foobar', txt2)
    with ppc.indent():
        ppc(txt)
        ppc('foobar', txt)
        with ppc.indent():
            ppc(txt)
            ppc('foobar', txt)
            with ppc.indent():
                ppc(txt)
                ppc(txt2)
                ppc('foobar', txt)
                ppc('foobar', txt2)

    result = ppc.flush()
    # print("\n" + result)
    for line in result.splitlines():
        assert len(line) <= 20
