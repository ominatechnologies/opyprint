import textwrap
from contextlib import contextmanager
from dataclasses import dataclass
from typing import Optional, Union, ClassVar
from inspect import isgenerator, signature
from re import compile

from .utils import is_dict, is_multiline, is_set, is_singleline

bullet_regex = compile('^([-><#@*]{1,3} )')


# TODO: support custom formatters
@dataclass
class PPContext:
    """
    Represents a pretty-printing context for constructing structured,
    human-readable representation of complex, composite data structures.

    This context provides three groups of methods and is callable itself.

    1. The :meth:`~format` method format objects and returns the resulting
       pretty-printed string.

    2. When calling a PPContext object as a function, then the given arguments
       are formatted and collected. Use the :meth:`~flush` method to get (and
       clear) the collected content.

       Example::

            def describe(pp: PPContext = None) -> str:
                pp = pp or PPContext()
                pp("A foobar object, with:")
                pp("* alpha", alpha)
                pp("* beta", beta)
                return pp.flush()

    3. The *context managers* (e.g. :meth:`~indent` or :meth:`~bullet`)
       temporarily adjust the pretty-print context.
    """

    # -- Class Initialization --------------- --- --  -

    default_width: ClassVar[int] = 120
    """The default content width, including indentation and bullets."""

    default_truncate: ClassVar[int] = 7
    """
    The default truncation setting. When this value is 0, no truncation is
    applied. When any other positive integer value *n* is given, then no more
    than *n* list/tuple/set elements or dictionary items will be included and
    no more than *n* lines of a wrapped string will be included.
    """

    default_bullet: ClassVar[str] = "- "
    """
    The default bullet prefix string that is used when using the
    :meth:`~bullet` context manager.
    """

    # -- Instance Initialization --------------- --- --  -

    __slots__ = [
        '_bullet',
        '_content_width',
        '_indent',
        '_lines',
        '_prefix_0',
        '_prefix_n',
        '_truncate',
        '_width',
    ]

    _bullet: Optional[str]
    _content_width: int
    _indent: str
    _lines: list
    _prefix_0: str
    _prefix_n: str
    _truncate: int
    _width: int

    def __init__(self,
                 width: int = default_width,
                 truncate: int = default_truncate,
                 bullet: str = "",
                 indent: str = ""):
        """
        :param width: Total width in characters, including bullets and
            indentation. Defaults to the value of the :attr:`~default_width`
            class attribute.
        :param truncate: The truncation setting. When this value is 0, no
            truncation is applied. When any other positive integer value *n* is
            given, then no more than *n* list/tuple/set elements or dictionary
            items will be included and no more than *n* lines of a wrapped
            string will be included. Defaults to the value of the
            :attr:`~default_truncate` class attribute.
        :param bullet: Optional bullet prefix string.
        :param indent: The indentation prefix string.
        """
        if not isinstance(width, int):
            msg = "Expected an int as 'width', got '{}'."
            raise TypeError(msg.format(width))

        if not isinstance(truncate, int):
            msg = "Expected an int as 'truncate', got '{}'."
            raise TypeError(msg.format(truncate))

        if not isinstance(bullet, str):
            msg = "Expected a string as 'bullet', got '{}'."
            raise TypeError(msg.format(bullet))

        if not isinstance(indent, str):
            msg = "Expected a string as 'indent', got '{}'."
            raise TypeError(msg.format(indent))

        self._bullet = self.normalize_bullet(bullet)
        self._indent = indent
        self._lines = list()
        self._truncate = truncate
        self._width = width

        self._update()

    def _update(self):
        if self._bullet:
            self._prefix_0 = self._indent + self._bullet
            self._prefix_n = self._indent + " " * len(self._bullet)
        else:
            self._prefix_0 = self._indent
            self._prefix_n = self._indent
        self._content_width = self._width - len(self._prefix_0)

    # -- Format Method and Helpers --------------- --- --  -

    def format(self, *args) -> str:
        """
        Returns a pretty-printed representation of the given arguments.

        :param args: Values to be formatted. When you provide one argument,
            then it will be pretty-printed normally. When you provide two
            arguments, then they will be formatted as a name-value pair (in a
            dict). When you provide three or more arguments, then these will be
            formatted as a list.
        """
        if len(args) == 1:
            arg = args[0]
            if isinstance(arg, str):
                result = arg
            else:
                result = self._format_aux(arg)
        elif len(args) == 2:
            result = self._format_aux({args[0]: args[1]})
        else:
            result = self._format_aux(args)

        if result is None:
            result = "--"
        elif not isinstance(result, str) or isinstance(result, list):
            msg = "Got an unexpected result from format_aux: '{}'"
            raise ValueError(msg.format(result))

        if self._bullet:
            if isinstance(result, str):
                result = result.splitlines()
            result[0] = self._prefix_0 + result[0]
            return ("\n" + self._prefix_n).join(result)

        if isinstance(result, list):
            result = "\n".join(result)

        if self._indent:
            return textwrap.indent(result, self._indent)

        return result

    def _format_aux(self, val) -> Union[str, list]:
        if self._indent or self._bullet:
            # Use a squashed context to cleanly format content that should
            # then be indented or bulleted:
            ppc = self._squash()
        else:
            ppc = self

        if isinstance(val, str):
            return ppc._format_str(val)
        if isinstance(val, list):
            return ppc._format_seq(val, "[", "]")
        if isgenerator(val):
            return ppc._format_seq(list(val), "[", "]")
        if isinstance(val, tuple):
            return ppc._format_seq(val, "(", ")")
        if is_set(val):
            return ppc._format_seq(list(val), "{", "}")
        if is_dict(val):
            return ppc._format_dict(val)

        describe = getattr(val, 'describe', None)
        if callable(describe):
            params = tuple(signature(describe).parameters.keys())
            if 'ppc' in params:
                if ppc == self:
                    # Use a fresh pp-context to pass to the describe method:
                    ppc = self._squash()
                try:
                    return val.describe(ppc=ppc)
                except TypeError:
                    pass
            elif 'width' in params:
                try:
                    return val.describe(width=ppc._content_width)
                except TypeError:
                    pass
            else:
                try:
                    return val.describe()
                except TypeError:
                    pass

        return str(val)

    def _format_str(self, val, quote: str = "\"") -> str:
        val = quote + val + quote
        if is_singleline(val) and len(val) > self._content_width:
            if self._truncate:
                max_len = self._content_width * self._truncate
                if len(val) > max_len:
                    val = textwrap.shorten(val, max_len)
            return textwrap.wrap(val, self._content_width)

        return val

    def _format_seq(self, seq, pal: str, par: str) -> str:
        if len(seq) == 0:
            return pal + par

        if self._truncate and len(seq) > self._truncate:
            seq = seq[:self._truncate].append("...")

        # Try to fit the items on one line:
        max_width = self._width - 2  # minus [], () or {}
        res = self.format(seq[0])
        if len(res) <= max_width and is_singleline(res):
            wrap = False
            for el in seq[1:]:
                res = res + ", " + self.format(el)
                if len(res) > max_width or is_multiline(res):
                    wrap = True
                    break
            if not wrap:
                return pal + res + par

        with self.bullet():
            return "\n".join(self.format(el) for el in seq)

    def _format_dict(self, dct):
        if len(dct) == 0:
            return "{}"

        kvs = [(key, dct[key]) for key in sorted(dct.keys())]

        truncated = False
        if self._truncate and len(kvs) > self._truncate:
            kvs = kvs[:self._truncate]

        lines = [self._format_kv_pair(k, v) for k, v in kvs]
        if truncated:
            lines.append("...")
        return "\n".join(lines)

    def _format_kv_pair(self, key, val):
        if isinstance(val, str):
            res = str(key) + ": " + val
            if len(res) <= self._content_width:
                return res

            if self._truncate:
                max_len = self._content_width * self._truncate
                if len(res) > max_len:
                    res = textwrap.shorten(res, max_len)

            lines = textwrap.wrap(res, self._content_width - 2)
            return "\n".join(lines[:1] + ["  " + line for line in lines[1:]])

        key = str(key)
        with self.indent():
            frm_val = self.format(val)

        lines = frm_val.splitlines()
        if len(lines) == 1:
            trimmed = frm_val.lstrip()
            if not bullet_regex.match(trimmed):
                res = key + ": " + trimmed
                if len(res) <= self._content_width:
                    return res
        elif (not isinstance(val, list)
              and not isinstance(val, tuple)
              and not is_set(val)
              and not is_dict(val)):
            trimmed = lines[0].lstrip()
            if not bullet_regex.match(trimmed):
                res = key + ": " + lines[0].lstrip()
                if len(res) <= self._content_width:
                    return res + "\n" + "\n".join(lines[1:])

        return key + ":\n" + frm_val

    # -- Context Managers --------------- --- --  -

    @contextmanager
    def indent(self, indent: str = "  "):
        ori_indent = self._indent
        self._indent = self._indent + indent
        ori_bullet = self._bullet
        self._bullet = ""
        self._update()
        try:
            yield self
        finally:
            self._indent = ori_indent
            self._bullet = ori_bullet
            self._update()

    @contextmanager
    def bullet(self, bullet: str = default_bullet):
        ori_bullet = self._bullet
        self._bullet = self.normalize_bullet(bullet)
        self._update()
        try:
            yield self
        finally:
            self._bullet = ori_bullet
            self._update()

    # -- Callable and Flush Methods --------------- --- --  -

    def __call__(self, *args) -> str:
        """
        Formats the given arguments and collects the resulting pretty-printed
        content. Call :meth:`~flush` to get the collected content.

        :param args: Values to be formatted. When you provide one argument,
            then it will be pretty-printed normally. When you provide two
            arguments, then they will be formatted as a name-value pair (in a
            dict). When you provide three or more arguments, then these will be
            formatted as a list.
        """
        result = self.format(*args)
        self._lines.append(result)
        return result

    def flush(self) -> str:
        """
        Returns (and clears) the pretty-printed content collected by calling
        the context as a function.
        """
        lines = self._lines
        self._lines = []
        return "\n".join(lines)

    # -- System Methods --------------- --- --  -

    @staticmethod
    def normalize_bullet(bullet: str) -> str:
        if bullet and not bullet.endswith(" "):
            return bullet + " "
        return bullet

    def _squash(self):
        """
        Get a new pp-context that has no bullet nor indent and whose width is
        the content-width of the current pp-context.
        """
        return PPContext(width=self._content_width,
                         truncate=self._truncate)
