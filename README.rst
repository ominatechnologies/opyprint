WPyPrint Readme
===============
An opinionated pretty-print library for Python.

Design Goals
------------
- You want to pretty-print complex data-structures that do not only consist
  of dicts, lists and other native data-structures and primitive values.
- You want to be able to write functions that carefully pretty-print
  your custom data types, with consistent indentation and wrapping when such
  objects occur in another data structure.
- You don't care about obtaining a pretty-printed form that can be used as
  input to the interpreter. Human readability is your main (and only) concern.
- You want some truncation control to limit the number of printed list
  elements, or the number of printed lines in wrapped strings.


Project Setup
-------------
We use pytest_ as testing framework and our code provides type hinting (see
PEP-484_ and PEP-561_) to enable static type checking using mypy_. For
test-driven development, we use pytest-watch_.

To install the package, use::

    $ pip install .

To install the package for development, use::

    $ pip install -r requirements.txt
    $ pip install --editable . | { grep -v "already satisfied" || :; }

To run the tests, use::

    $ python -m pytest

For test-driven development, use::

    $ pytest-watch

Roadmap
-------
See `<TODO.rst>`_.


.. _mypy: http://mypy-lang.org
.. _PEP-484: https://www.python.org/dev/peps/pep-0484
.. _PEP-561: https://www.python.org/dev/peps/pep-0561
.. _pytest: https://docs.pytest.org
.. _pytest-watch: https://github.com/joeyespo/pytest-watch
.. _setuptools: https://setuptools.readthedocs.io
