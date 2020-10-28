OPyPrint Readme
===============
.. inclusion-marker

An opinionated pretty-printing library for Python.

`API-Docs <https://ominatechnologies.github.io/opyprint/>`_

Design Goals
------------
- You want to pretty-print complex data-structures that do not only consist
  of dicts, lists and other native data-structures and primitive values, but
  also includes custom data types.
- You want to be able to write functions that carefully pretty-print
  your custom data types, with consistent indentation and wrapping when such
  objects occur nested in other data structure.
- You don't care about obtaining a pretty-printed form that can be used as
  input to the interpreter. Human readability is your main (and only) concern.
- You want some truncation control to limit the number of printed list
  elements, or the number of printed lines in wrapped strings.

Usage
-----
To pretty-print native data-structures you want to use the 'print' function
provided in this package instead of the native 'print' function provided in
Python. This custom 'print' function is a drop-in replacement that support all
the keyword-arguments supported by the native function.

>>> from opyprint import print
>>> print({'alpha': [1, 2, 3], 'beta': "satisfied"})
- alpha: [1, 2, 3]
- beta: satisfied

To support pretty-printing in your custom data types, you need to implement
their '__str__' method as follows:

- The method should accept a *PPContext* object as ``ppc`` keyword argument. It
  should default to ``None``, in which case the pp-context object should be
  initialized in the method body.
- Use the ``ppc`` object (as a function) to add formatted content in the
  context queue.
- Return the result of ``ppc.flush()``, as shown in the following example::

    class Alpha:
        def __init__(self, prop_1, prop_2):
            self.prop_1 = prop_1
            self.prop_2 = prop_2

        def __str__(self, ppc: PPContext = None):
            ppc = ppc or PPContext()
            ppc("An Alpha object with:")
            with ppc.bullets():
                ppc("prop_1", self.prop_1)
                ppc("prop_2", self.prop_2)
            return ppc.flush()

Project Setup
-------------
This project requires Python 3.7 or higher. It is supported for Python 3.7, 3.8
and 3.9.

This project uses pytest_ as testing framework and our code provides type
hinting (see PEP-484_ and PEP-561_) to enable static type checking using mypy_.
For test-driven development, we use pytest-watch_. We use flake8_ for code
linting. Linting and static type checking are integrated in the standard
pytest_-managed testing.

This project uses sphinx_ to generate its documentation. To be able to build
the docs as latex/pdf, you need to install the proper tex tools.
On MacOS, install MacTex_ and latexmk_.

To install the package for normal use in your application, use::

    $ pip install .

To run the tests, use::

    $ pip install -r requirements.test.txt
    $ pip install --editable .
    $ python3 -m pytest

or::

    $ tox -e pytest-dev-py38

For test-driven development, use::

    $ pip install -r requirements.test.txt
    $ pip install --editable .
    $ pytest-watch

To enforce code formatting, install the git hook::

    $ flake8 --install-hook git
    $ git config --bool flake8.strict true

To build the docs as html, use::

    $ tox -e pytest-html

To build the docs as pdf, use::

    $ tox -e pytest-pdf

Pytest, mypy and flake8 are configured in the *setup.cfg* file. Sphinx and
its plugins are configured in *docs/conf.py*.


.. _flake8: http://flake8.pycqa.org
.. _latexmk: https://mg.readthedocs.io/latexmk.html
.. _MacTex: http://www.tug.org/mactex/mactex-download.html
.. _mypy: http://mypy-lang.org
.. _PEP-484: https://www.python.org/dev/peps/pep-0484
.. _PEP-561: https://www.python.org/dev/peps/pep-0561
.. _pytest: https://docs.pytest.org
.. _pytest-watch: https://github.com/joeyespo/pytest-watch
.. _setuptools: https://setuptools.readthedocs.io
.. _sphinx: http://www.sphinx-doc.org
