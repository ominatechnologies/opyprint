Changelog
=========

.. inclusion-marker

v0.1 - 2019-01-02
+++++++++++++++++
- Added the 'PPContext' class and the 'print' function.


v0.2 - 2019-01-06
+++++++++++++++++
- Name-value pairs are now also bulletted.
- Added optional 'bullet' parameter for the '__call__', 'format' and 'print'
  methods.


v0.3 - 2019-01-07
+++++++++++++++++
- Added 'bullet' and 'width' parameters for the 'print' function.


v0.4 - 2020-01-09
+++++++++++++++++
- The 'print' function is now a proper drop-in replacement for the native one.
- Added support for implementations of the '__str__' method that take an
  optional 'PPContext' object as parameters.


Next
++++
- Added 'lt' and 'dict_lt' utilities.
- Added Sphinx-based docs.
- Added code linting using Flake8.
