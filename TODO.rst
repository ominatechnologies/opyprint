WPyPrint TODO
#############

Must Haves
**********

Should Haves
************
- Users can add custom formatters.

Could Haves
***********


Proposal
********
I would like to propose the following small and non-breaking change:

In the 'textwrap.indent' function, pass the line index as second argument to
the predicate. This non-breaking change would allow developers to, for example,
indent all but the first line in an efficient manner as shown in the following
hypothetical example:

>>> s = 'l1\nl2\nl3'
>>> indent(s, '  ', predicate=lambda line, index: index > 0)
'l1\n  l2\n  l3'
