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


v0.5 - 2020-01-11
+++++++++++++++++
- Added Sphinx-based docs.
- Added 'lt' and 'dict_lt' utilities.
- Added code linting using Flake8.


v0.6 - 2020-01-14
+++++++++++++++++
- Renamed 'wpyprint' to 'opyprint'.
- Various improvements.


v0.7 - 2020-03-23
+++++++++++++++++
- Add support for styled formatting.
- Upgrade to Python v3.8.
- Migrated to our own frozendict.


v0.8 - 2020-04-13
+++++++++++++++++
- Add support for 'indent', 'style' and 'truncate' parameters in the 'print'
  function replacement.


Head
++++
- feat: Explicitly support the parameters for the native 'print' function for
  its drop-in replacement to improve auto-completion and documentation.
- fix: Handle classes that implement a 'describe' method that does not return
  a string.
