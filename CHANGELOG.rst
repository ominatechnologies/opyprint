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


v0.9 - 2020-05-26
+++++++++++++++++
- feat: Add 'key_style' option.
- feat: Add additional styling options.
- feat: Explicitly support the parameters for the native 'print' function for
  its drop-in replacement to improve auto-completion and documentation.
- fix: Handle classes that implement a 'describe' method that does not return
  a string.


v0.10 - 2020-06-02
++++++++++++++++++
- feat: Add additional color styling options.


v0.11 - 2020-06-03
++++++++++++++++++
- refactor: Change the color naming scheme.


v0.12 - 2020-06-08
++++++++++++++++++
- feat: Add the 'Logger', 'PrintLogger' and 'VoidLogger' classes (copied from
  'hails').
- feat: Add the 'LoggedMixin' mixin class.
- feat: Add the 'debug_indent' and the 'trace_indent' methods in the 'Logger'
  class.
- feat: Add the 'format' utility.


v0.13 - 2020-09-06
++++++++++++++++++
- feat: Add the 'truncate' parameter for the 'Logger' constructor.
- feat: Add the `with PPContext.truncate` context manager, add the
  `PPContext.truncation` property, and add support for the `truncate` parameter
  in `PPContext.__call__`, `Logger.debug`, `Logger.trace` and `Logger.info`.
- feat: Accept `>` as key demarcation character.
- fix: Use white text instead of default text color on colored background in
  the logging.
- fix: Use the default string representation for class objects and do not try
  to delegate to the describe method.
- chore: Update dependencies.


2020.10.14
++++++++++
- fix: Various minor improvements and fixes.
- chore: Update dependencies.


2020.11.25
++++++++++
- fix: Various improvements and fixes.
- setup: Add tox-based testing.
- chore: Update dependencies.


Head
++++
