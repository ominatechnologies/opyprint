WPyPrint Readme
===============
An opinionated pretty-print library for Python.

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
