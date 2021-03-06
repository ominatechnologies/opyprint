# test_a_basics

from pytest import raises

from opyprint import PPContext


def test_brackets():
    assert PPContext._brackets(set()) == ("{", "}")
    assert PPContext._brackets(tuple()) == ("(", ")")
    assert PPContext._brackets(list()) == ("[", "]")
    assert PPContext._brackets((v for v in [1, 2, 3])) == ("[", "]")
    assert PPContext._brackets(range(0, 10)) == ("[", "]")


def test_normalize_bullet():
    ppc = PPContext()
    assert ppc._normalize_bullet(True) == PPContext.default_bullet
    assert ppc._normalize_bullet(False) == ""
    assert ppc._normalize_bullet(None) == ""
    assert ppc._normalize_bullet() == ""
    assert ppc._normalize_bullet("") == ""
    # noinspection PyTypeChecker
    assert ppc._normalize_bullet(123) == PPContext.default_bullet
    assert ppc._normalize_bullet("-") == "- "
    assert ppc._normalize_bullet("- ") == "- "
    assert ppc._normalize_bullet("--") == "- "
    assert ppc._normalize_bullet("---") == "- "
    assert ppc._normalize_bullet(">") == "> "
    assert ppc._normalize_bullet(">>") == "> "
    assert ppc._normalize_bullet(">>>") == "> "
    assert ppc._normalize_bullet("#") == "# "
    assert ppc._normalize_bullet("##") == "# "
    assert ppc._normalize_bullet("###") == "# "

    with ppc.bullets("*"):
        assert ppc._normalize_bullet(True) == "* "
        assert ppc._normalize_bullet("-") == "- "


def test_init_error_1():
    with raises(TypeError):
        # noinspection PyTypeChecker
        PPContext(width=1.5)

    with raises(TypeError):
        # noinspection PyTypeChecker
        PPContext(truncate=1.5)

    with raises(TypeError):
        # noinspection PyTypeChecker
        PPContext(indent=1.5)

    with raises(TypeError):
        # noinspection PyTypeChecker
        PPContext(bullet=1.5)


def test_indentation():
    ppc = PPContext()
    assert ppc.indentation == ""

    ppc = PPContext(indent="    ")
    assert ppc.indentation == "    "
    ppc.indentation = "..."
    assert ppc.indentation == "..."
