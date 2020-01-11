import textwrap
from contextlib import contextmanager
from dataclasses import dataclass
from inspect import isgenerator, signature
from re import compile
from typing import ClassVar, Generator, List, Optional, Tuple, Union

from .utils import is_dict, is_multiliner, is_oneliner, is_set, is_tuple


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
       clear) the collected content or the :meth:`~print` method to print (and
       clear) the collected content.

       Example::

            def describe(ppc: PPContext = None) -> str:
                ppc = ppc or PPContext()
                ppc("A foobar object, with:")
                ppc("* alpha", alpha)
                ppc("* beta", beta)
                return ppc.flush()

    3. The *context managers* (e.g. :meth:`~indent` or :meth:`~bullet`)
       temporarily adjust the pretty-print context.
    """

    # -- Class Initialization --------------- --- --  -

    bullet_regex = compile('^([-+=|:~<>#$%^&@*?!]{1,3} )')
    """
    A compiled regular expression that is used to determine if a formatted
    string starts with a bullet.
    """

    default_width: ClassVar[int] = 100
    """The default content width, including indentation and bullets."""

    default_truncate: ClassVar[int] = 7
    """
    The default truncation setting. When this value is 0, no truncation is
    applied. When any other positive integer value *n* is given, then no more
    than *n* list/tuple/set elements or dictionary items will be included and
    no more than *n* lines of a wrapped string will be included.
    """

    default_bullet: ClassVar[str] = "- "
    """The default bullet prefix string."""

    default_indent: ClassVar[str] = "  "
    """The default single indentation string."""

    print_name_value_pairs: ClassVar[bool] = True
    """
    When true, calling the :meth:`~print` method with two arguments will
    print them as a name-value pair.
    """

    # -- Instance Initialization --------------- --- --  -

    __slots__ = [
        '_bullet',
        '_content_width',
        '_default_bullet',
        '_indent',
        '_lines',
        '_prefix_0',
        '_prefix_n',
        '_truncate',
        '_width',
    ]

    _bullet: Optional[str]
    _content_width: int
    _default_bullet: str
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
                 indent: str = "",
                 default_bullet: str = default_bullet):
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

        self._bullet = None
        self._bullet = self._normalize_bullet(bullet) if bullet else ""
        self._indent = indent
        self._lines = list()
        self._truncate = truncate
        self._width = width

        # Manage an instance-level default bullet to allow it to be customized,
        # such as when providing the 'bullet' argument to the 'format' method:
        self._default_bullet = default_bullet

        self._update()

    # -- Accessors --------------- --- --  -

    @property
    def indentation(self) -> str:
        """The current indentation string."""
        return self._indent

    @indentation.setter
    def indentation(self, indent: str):
        """Set the current indentation string."""
        self._indent = indent
        self._update()

    # -- Format Method and Helpers --------------- --- --  -

    def format(self, *args, bullet: Union[str, bool] = None) -> str:
        """
        Returns a pretty-printed representation of the given arguments.

        :param args: Values to be formatted. When you provide one argument,
            then it will be pretty-printed normally. When you provide two
            arguments, then they will be formatted as a name-value pair (in a
            dict). When you provide three or more arguments, then these will be
            formatted as a list.
        :param bullet: When given, prefix the formatted result with a bullet,
            when this is not yet the case. The argument may be either a
            non-empty string, the first character of which is taken
            as the bullet, or true to use the current or default bullet.
        """
        if len(args) == 0:
            return ""

        if len(args) == 1:
            obj = args[0]
        elif len(args) == 2 and self.print_name_value_pairs:
            obj = {args[0]: args[1]}
        else:
            obj = args

        if bullet:
            bullet = self._normalize_bullet(bullet)
            if self._is_bullettable(obj):
                return self._format_aux(obj, bullet=bullet)
            elif self._bullet != bullet:
                ori_bullet = self._bullet
                self._bullet = bullet
                self._update()
                result = self._format_aux(obj)
                self._bullet = ori_bullet
                self._update()
                return result
            else:
                return self._format_aux(obj)
        else:
            return self._format_aux(obj)

    def _format_aux(self, obj, bullet: str = None) -> str:
        result = self._format_dispatch(obj, bullet=bullet)

        if not isinstance(result, str) and not isinstance(result, list):
            msg = ("Got an unexpected result of type '{}' from the formatter:"
                   "\n  - the given object: {}"
                   "\n  - the formatted result: {}")
            raise ValueError(msg.format(type(result), obj, result))

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

    def _format_dispatch(self, obj, bullet: str = None) -> Union[str, list]:
        if self._indent or self._bullet:
            # Use a squashed context to cleanly format content that should
            # then be indented or bulleted:
            ppc = self._squash()
        else:
            ppc = self

        if isinstance(obj, str):
            return ppc._format_str(obj)
        if is_dict(obj):
            return ppc._format_dict(obj, bullet)
        if self._is_bullettable(obj):
            return ppc._format_bullettable(obj, bullet=bullet)

        # pass the ppcontext to __str__ when possible:
        __str__ = getattr(obj, '__str__', None)
        if (callable(__str__) and
                'ppc' in tuple(signature(__str__).parameters.keys())):
            if ppc == self:
                # Use a fresh pp-context to pass to the __str__ method:
                ppc = self._squash()
            return obj.__str__(ppc=ppc)

        # use the 'describe' method when it is provided (deprecated):
        describe = getattr(obj, 'describe', None)
        if callable(describe):
            params = tuple(signature(describe).parameters.keys())
            if 'ppc' in params:
                if ppc == self:
                    # Use a fresh pp-context to pass to the describe method:
                    ppc = self._squash()
                return obj.describe(ppc=ppc)
            elif 'width' in params:
                return obj.describe(width=ppc._content_width)
            else:
                return obj.describe()

        return str(obj)

    def _format_str(self, obj) -> str:
        if obj == "":
            return obj

        if is_oneliner(obj) and len(obj) > self._content_width:
            if self._truncate:
                max_len = self._content_width * self._truncate
                if len(obj) > max_len:
                    obj = textwrap.shorten(obj, max_len)
            return textwrap.wrap(obj, self._content_width)

        return obj

    def _format_dict(self, dct, bullet: str = None):
        if len(dct) == 0:
            return "{}"
        elif len(dct) == 1:
            for key in dct:
                return self._format_kv_pair(key, dct[key], bullet)
        else:
            kvs = [(key, dct[key]) for key in sorted(dct.keys())]

            truncated = False
            if self._truncate and len(kvs) > self._truncate:
                kvs = kvs[:self._truncate]
                truncated = True

            bullet = bullet or self._default_bullet
            lines = [self._format_kv_pair(k, v, bullet) for k, v in kvs]
            if truncated:
                lines.append(bullet + "...")
            return "\n".join(lines)

    def _format_kv_pair(self, key, value, bullet: str = ""):
        bullet = bullet or ""
        bullet_len = len(bullet)

        # Format the key, truncating it when it is too long:
        key = str(key)
        max_key_length = max(int((self._content_width - bullet_len) / 2), 10)
        if len(key) > max_key_length:
            key = key[:max_key_length - 3] + "..."

        # Format a key-value pair with a string value, which is assumed to be
        # regular text, as a oneliner or a wrapped and indented multiliner:
        if isinstance(value, str):
            # try to format the keyed string as a oneliner:
            result = bullet + str(key) + ": " + value
            if len(result) <= self._content_width:
                return result

            result = textwrap.wrap(
                result,
                width=self._content_width - bullet_len,
                subsequent_indent=self.default_indent + " " * bullet_len,
                max_lines=self._truncate)
            return "\n".join(result)

        # Try to format as a oneliner when the formatted value is a
        # oneliner, except when the value is a key-value mapping or the
        # formatted value seems to be bulletted:
        if not is_dict(value):
            result = self.format(value)
            if is_oneliner(result) and not self.bullet_regex.match(result):
                result = bullet + key + ": " + result
                if len(result) <= self._content_width:
                    return result

        # Format multiline value with indentation:
        with self.indent(self.default_indent + " " * bullet_len):
            result = self.format(value)

        # Try to fit the first line on the same line as the key, except when
        # the value is a key-value mapping or the formatted value seems
        # to be bulletted:
        if not is_dict(value):
            lines = result.splitlines()
            trimmed = lines[0].lstrip()
            if not self.bullet_regex.match(trimmed):
                first = bullet + key + ": " + trimmed
                if len(first) <= self._content_width:
                    return first + "\n" + "\n".join(lines[1:])

        return bullet + key + ":\n" + result

    def _format_bullettable(self, items, bullet: str = None) -> str:
        brl, brr = self._brackets(items)
        if isgenerator(items):
            items = self._generate_items(items)
        elif self._truncate and len(items) > self._truncate:
            if is_set(items):
                items = list(items)
                # noinspection PyBroadException
                try:
                    items = sorted(items)
                except Exception:
                    pass
                items = items[:self._truncate]
                items.append("...")
            elif isinstance(items, tuple):
                items = list(items)[:self._truncate]
                items.append("...")
            elif is_dict(items):
                raise Exception("Unexpected")
            else:
                items = items[:self._truncate]
                items.append("...")
        elif is_set(items):
            items = list(items)
            # noinspection PyBroadException
            try:
                items = sorted(items)
            except Exception:
                pass

        if len(items) == 0:
            return brl + brr

        # Try to format as a bracketed oneliner:
        result = self._format_oneliner(items, brl, brr, bullet=bullet)
        if result:
            return result

        # Format as bulletted items:
        with self.bullets(bullet=bullet):
            return "\n".join(self.format(el) for el in items)

    def _format_oneliner(self, items, brl, brr, bullet: str = None) -> \
            Optional[str]:
        max_width = self._width - 2  # minus the _brackets
        if bullet:
            max_width -= len(bullet)  # minus the bullet

        result = ""
        for item in items:
            frm_item = self.format(item)
            if is_multiliner(frm_item):
                return
            if not result:
                result = frm_item
            else:
                result = result + ", " + frm_item

            if len(result) > max_width:
                return

        if bullet:
            return bullet + brl + result + brr
        else:
            return brl + result + brr

    # -- Context Managers --------------- --- --  -

    @contextmanager
    def indent(self, indent: str = default_indent):
        """
        Indents the pretty-printing context.

        Use this context-manager in a ``with`` statement as shown in the
        following example::

            ppc = PPContext()
            ppc("v1")
            with ppc.indent():
                ppc("v2")
                ppc("v3")
            ppc("v4")
            ppc.print()

        The above will print the following::

            v1
              v2
              v3
            v4

        :param indent: The optional indentation prefix string. Defaults to the
            value of the static :attr:`~default_indent` attribute.
        """
        ori_bullet = self._bullet
        ori_indent = self._indent
        if not self._bullet:
            self._indent = self._indent + indent
        self._bullet = ""
        self._update()
        try:
            yield self
        finally:
            self._bullet = ori_bullet
            self._indent = ori_indent
            self._update()

    @contextmanager
    def bullets(self, bullet: str = None):
        """
        Prefixes each formatted object in the pretty-printing context with a
        bullet.

        Use this context-manager in a ``with`` statement as shown in the
        following example::

            ppc = PPContext()
            ppc("v1")
            with ppc.bullet():
                ppc("v2")
                ppc("v3")
            ppc("v4")
            ppc.print()

        The above will print the following::

            v1
            - v2
            - v3
            v4

        :param bullet: The bullet prefix string. Defaults to the value of
            the static :attr:`~default_bullet` attribute or when this context
            is nested in another 'bullets' context, the bullet for that
            context.
        """
        ori_bullet = self._bullet
        ori_indent = self._indent
        if self._bullet:
            self._indent = self._indent + "  "
        self._bullet = self._normalize_bullet(bullet or True)
        self._update()
        try:
            yield self
        finally:
            self._bullet = ori_bullet
            self._indent = ori_indent
            self._update()

    # -- Callable, print and flush Methods --------------- --- --  -

    def __call__(self, *args, bullet: Union[str, bool] = None) -> None:
        """
        Formats the given arguments and collects the resulting pretty-printed
        content. Call :meth:`~flush` to get (and clear) the collected content
        or :meth:`~print` to print (and clear) the collected content.

        Example::

            ppc = PPContext()
            ppc("v1")
            ppc("v2")
            ppc("v3")
            ppc("v4")
            ppc.print()

        The above will print the following::

            v1
            v2
            v3
            v4

        :param args: The values to format. When you provide one argument,
            then it will be pretty-printed normally. When you provide two
            arguments and the static :attr:`~print_name_value_pairs` attribute
            is true, then they will be formatted as a name-value pair. When you
            provide three or more arguments, then these will be formatted as a
            (oneliner or bulletted) list.
        :param bullet: When given, prefix the formatted result with a bullet
            when this is not yet the case. The argument may be either a
            non-empty string, the first character of which is taken
            as the bullet, or true to use the current or default bullet.
        """
        self._lines.append(self.format(*args, bullet=bullet))

    def newline(self) -> None:
        """Adds a newline in the collected content."""
        self._lines.append("")

    def flush(self) -> str:
        """
        Returns (and clears) the pretty-printed content collected by calling
        the context as a function.
        """
        lines = self._lines
        self._lines = []
        return "\n".join(lines)

    def print(self, *args, bullet: Union[str, bool] = None, **kwargs) -> None:
        """
        Pretty-prints the given arguments or the pretty-printed content
        collected by calling the context as a function.

        Additional keyword arguments are passed to the native Python 'print'
        function.

        :param args: When called without arguments the pretty-printed
            content collected by calling the context as a function is printed.
            When called with two argument and the
            :attr:`~print_name_value_pairs` attributes is true, then the
            arguments are printed as a name-value pair (in a dict). Otherwise
            multiple arguments are printed as list.
        :param bullet: When given, prefix the formatted result with bullet,
            when this is not yet the case. The argument may be either a
            non-empty string, the first character of which is taken
            as the bullet, or true to use the current or default bullet.
            This parameter is ignored when this method is called with (other)
            arguments.
        """
        if len(args) == 0:
            print(self.flush(), **kwargs)
        else:
            print(self.format(*args, bullet=bullet), **kwargs)

    # -- System Methods --------------- --- --  -

    def _update(self):
        if self._bullet:
            self._prefix_0 = self._indent + self._bullet
            self._prefix_n = self._indent + " " * len(self._bullet)
        else:
            self._prefix_0 = self._indent
            self._prefix_n = self._indent
        self._content_width = self._width - len(self._prefix_0)

    @staticmethod
    def _is_bullettable(obj) -> bool:
        """
        Checks if the pretty-printed representation of the given object is
        normally bulletted.

        :param obj: The value to check.
        """
        if (isinstance(obj, str)
                or isinstance(obj, bytes)
                or isinstance(obj, bytearray)
                or isinstance(obj, memoryview)):
            return False
        else:
            return hasattr(obj, '__iter__')

    @staticmethod
    def _brackets(obj) -> Tuple[str, str]:
        """Gets the appropriate _brackets for the given bullettable object."""
        if is_set(obj):
            return "{", "}"
        elif is_tuple(obj):
            return "(", ")"
        else:
            return "[", "]"

    def _normalize_bullet(self, bullet: Union[str, bool] = None) -> str:
        """
        Normalizes the given bullet string.

        A normalized bullet string consists of one character followed by a
        single space.

        - When a non-empty string is given, the first character is taken as the
          bullet.
        - When true is given, the current or default bullet is used.
        - When an empty string or false is given, a (falsy) empty string is
          returned.
        """
        if isinstance(bullet, str):
            if len(bullet) == 1:
                return bullet + " "
            if len(bullet) == 2 and not bullet.endswith(" ") or len(
                    bullet) > 2:
                return bullet[:1] + " "
            return bullet
        elif bullet:
            return self._bullet or self._default_bullet
        else:
            return ""

    def _squash(self):
        """
        Get a new pp-context that has no bullet nor indent and whose width is
        the content-width of the current pp-context.
        """
        return PPContext(width=self._content_width,
                         truncate=self._truncate,
                         default_bullet=self._default_bullet)

    def _generate_items(self, generator: Generator) -> List:
        # Warning: The generator will be (partially) exhausted.
        if self._truncate:
            items = list()
            try:
                for i in range(self._truncate):
                    items.append(next(generator))
                items.append("...")
            except StopIteration:
                pass
            return items
        return list(generator)
