from __future__ import annotations

from abc import ABC, abstractmethod
from contextlib import contextmanager
from typing import ClassVar, Optional, Protocol, runtime_checkable

from ..pp_context import PPContext
from ..pp_styles import PPStyles
from ..typing import StyleOptions


@runtime_checkable
class Logger(Protocol):
    """Abstract base class for concrete Logger classes."""

    # -- Class Vars and Methods ---------------- --- --  -

    DISABLED: ClassVar[int] = 0
    DEBUG: ClassVar[int] = 1
    TRACE: ClassVar[int] = 2
    INFO: ClassVar[int] = 3

    Void: ClassVar[Logger]

    # -- Accessors ---------------- --- --  -

    @property
    @abstractmethod
    def enabled(self) -> bool:
        """
        True when the logger is enabled, i.e. when the log level is not 0.
        """
        raise NotImplementedError()

    @property
    def debug_enabled(self) -> bool:
        """True when the 'debug' log level is enabled."""
        raise NotImplementedError()

    @property
    def trace_enabled(self) -> bool:
        """True when the 'trace' log level is enabled."""
        raise NotImplementedError()

    @property
    def info_enabled(self) -> bool:
        """True when the 'info' log level is enabled."""
        raise NotImplementedError()

    @property
    def disabled(self) -> bool:
        """
        True when the logger is disabled, i.e. when the log level is 0.
        """
        raise NotImplementedError()

    @property
    def indent_depth(self) -> int:
        """
        The number of space characters the current indentation consists of.
        """
        raise NotImplementedError()

    @property
    def indentation(self) -> str:
        """The current indentation string."""
        raise NotImplementedError()

    @property
    def level(self) -> int:
        """The current log level."""
        raise NotImplementedError()

    @level.setter
    def level(self, level: int) -> None:
        raise NotImplementedError()

    @property
    def width(self) -> int:
        """The current width at which line breaking is preferred."""
        raise NotImplementedError()

    @property
    def parent(self) -> Optional[Logger]:
        """The parent logger."""
        raise NotImplementedError()

    @parent.setter
    def parent(self, parent: Logger) -> None:
        raise NotImplementedError()

    @property
    def ppc(self) -> PPContext:
        """The pretty-print context object."""
        raise NotImplementedError()

    # -- Abstract Methods ---------------- --- --  -

    def handle_log(self,
                   *msgs,
                   bullet: str = None,
                   indent: str = "",
                   key_style: StyleOptions = None,
                   level: int = TRACE,
                   margin: int = 0,
                   style: StyleOptions = None,
                   truncate: int = None) -> None:
        """
        Handle a log message.

        :param msgs: The messages.
        :param bullet: Optional bullet.  See opyprint.pp_context for more
            details.
        :param indent: The indentation prefix string. See opyprint.pp_context
            for more details.
        :param key_style: Optional style specifications for the key part of
            key-value pairs. See opyprint.pp_context for more details.
        :param level: Optional log level.
        :param margin: Optional margin.
        :param style: Optional styling. See opyprint.pp_context for more
            details.
        :param truncate: Optional truncation. See opyprint.pp_context for more
            details.
        """
        raise NotImplementedError()

    # -- Methods ---------------- --- --  -

    def enable(self, level: int = 2) -> Logger:
        """Enable the LOGGER and set the given log level (default: "trade")."""
        raise NotImplementedError()

    def disable(self) -> Logger:
        """Disable the LOGGER."""
        raise NotImplementedError()

    @contextmanager
    def indent(self):
        """
        Increase the indentation for the subsequent log calls if the log level
        is info or higher.
        """
        raise NotImplementedError()

    @contextmanager
    def debug_indent(self):
        """
        Increase the indentation for the subsequent log calls if the log level
        is debug or higher.
        """
        raise NotImplementedError()

    @contextmanager
    def trace_indent(self):
        """
        Increase the indentation for the subsequent log calls if the log level
        is debug or higher.
        """
        raise NotImplementedError()

    def indent_once(self, to: int = None):
        """Increase the indentation for the subsequent log calls."""
        raise NotImplementedError()

    def dedent(self):
        """Decrease the indentation for the subsequent log calls."""
        raise NotImplementedError()

    def debug(self,
              *msgs,
              bullet: str = None,
              indent: str = "",
              key_style: StyleOptions = None,
              margin: int = 0,
              style: StyleOptions = None,
              truncate: int = None) -> None:
        """
        Log at level 1.

        :param msgs: The messages.
        :param bullet: Optional bullet.
        :param indent: The indentation prefix string.
        :param key_style: Optional style specifications for the key part of
            key-value pairs.
        :param margin: Optional margin.
        :param style: Optional styling.
        :param truncate: Optional truncation.
        """
        raise NotImplementedError()

    def trace(self,
              *msgs,
              bullet: str = None,
              indent: str = "",
              key_style: StyleOptions = None,
              margin: int = 0,
              style: StyleOptions = None,
              truncate: int = None) -> None:
        """
        Log at level 2.

        :param msgs: The messages.
        :param bullet: Optional bullet.
        :param indent: The indentation prefix string.
        :param key_style: Optional style specifications for the key part of
            key-value pairs.
        :param margin: Optional margin.
        :param style: Optional styling.
        :param truncate: Optional truncation.
        """
        raise NotImplementedError()

    def info(self,
             *msgs,
             bullet: str = None,
             indent: str = "",
             key_style: StyleOptions = None,
             margin: int = 0,
             style: StyleOptions = None,
             truncate: int = None) -> None:
        """
        Log at level 3.

        :param msgs: The messages.
        :param bullet: Optional bullet.
        :param indent: The indentation prefix string.
        :param key_style: Optional style specifications for the key part of
            key-value pairs.
        :param margin: Optional margin.
        :param style: Optional styling.
        :param truncate: Optional truncation.
        """
        raise NotImplementedError()

    def log(self,
            *msgs,
            bullet: str = None,
            indent: str = "",
            key_style: StyleOptions = None,
            level: int = TRACE,
            margin: int = 0,
            style: StyleOptions = None,
            truncate: int = None) -> None:
        """
        Log at the given level.

        :param msgs: The messages. When you provide one argument,
            then it will be pretty-printed normally. When you provide two
            arguments, then they will be formatted as a name-value pair (in a
            dict). When you provide three or more arguments, then these will be
            formatted as a list.
        :param bullet: Optional bullet.
        :param indent: The indentation prefix string.
        :param key_style: Optional style specifications for the key part of
            key-value pairs.
        :param level: Optional log level.
        :param margin: Optional margin.
        :param style: Optional styling.
        :param truncate: Optional truncation.
        """
        raise NotImplementedError()

    def reset(self) -> None:
        """Resets the LOGGER, i.e. resets indentation to 0."""
        raise NotImplementedError()

    # noinspection PyShadowingBuiltins
    def log_connectum(self,
                      cnm,
                      *,
                      all: bool = False,
                      bindings=False,
                      binding_sources: bool = False,
                      checked: bool = False,
                      history: bool = False,
                      label: str = None,
                      level: int = DEBUG,
                      resolve_state: bool = True,
                      sub_connecta: bool = True,
                      truncate: int = 0) -> None:
        """
        Log the given connectum.

        :param all: Include all details, i.e. bindings, binding_sources,
            checked, history, resolve state and sub-connecta.
        :param cnm: The connectum to log.
        :param bindings: Provide true (the default) to include the bindings.
        :param binding_sources: Include the binding source information. Implies
            bindings.
        :param checked: Include the gate and link 'checked' status.
        :param history: Include the resolve/build history.
        :param label: Optional connectum label.
        :param level: The logger level.
        :param resolve_state: Include the blocks' resolve state.
        :param sub_connecta: Provide true (the default) to include
            recursive descriptions of the composite sub-connecta.
        :param truncate: The truncation setting. When this value is 0, no
            truncation is applied. When any other positive integer value *n* is
            given, then no more than *n* list/tuple/set elements or dictionary
            items will be included and no more than *n* lines of a wrapped
            string will be included. Defaults to 0.
        """
        raise NotImplementedError()


class LoggerBase(Logger, ABC):
    """Base class for concrete Logger classes."""

    # -- Class Vars and Methods ---------------- --- --  -

    DISABLED: ClassVar[int] = 0
    DEBUG: ClassVar[int] = 1
    TRACE: ClassVar[int] = 2
    INFO: ClassVar[int] = 3

    Void: ClassVar[Logger]

    # -- Instance Initialization ---------------- --- --  -

    __slots__ = [
        "_indent",
        "_level",
        "_log_history",
        "_log_resolve_state",
        "_parent",
        "_ppc",
        "_width",
    ]

    _indent: int
    _level: int
    _ppc: PPContext
    _width: int

    def __init__(self,
                 level: int = 2,
                 log_history: bool = False,
                 log_resolve_state: bool = True,
                 parent: Logger = None,
                 truncate: int = 0,
                 width: int = 100):
        """
        :param level: log level
        :param log_history: See 'log_connectum' method.
        :param log_resolve_state: See 'log_connectum' method.
        :param parent: When given, the indentation of this parent logger is
            added to the indentation of this "dependent" logger.
        :param truncate: The truncation setting. When this value is 0, no
            truncation is applied. When any other positive integer value *n* is
            given, then no more than *n* list/tuple/set elements or dictionary
            items will be included and no more than *n* lines of a wrapped
            string will be included.
        :param width: max content width
        """
        self._indent = 0
        self._level = level
        self._log_history = log_history
        self._log_resolve_state = log_resolve_state
        self._parent = parent
        self._ppc = PPContext(width=width, truncate=truncate)
        self._width = width

    # -- Accessors ---------------- --- --  -

    @property
    def enabled(self):
        return self._level > 0

    @property
    def debug_enabled(self):
        return 0 < self._level <= Logger.DEBUG

    @property
    def trace_enabled(self):
        return 0 < self._level <= Logger.TRACE

    @property
    def info_enabled(self):
        return 0 < self._level <= Logger.INFO

    @property
    def disabled(self):
        return self._level == 0

    @property
    def indent_depth(self):
        if self._parent:
            return self._parent.indent_depth + self._indent
        else:
            return self._indent

    @property
    def indentation(self):
        if self.parent:
            return self.parent.indentation + self.ppc.indentation
        else:
            return self.ppc.indentation

    @property
    def level(self):
        return self._level

    @level.setter
    def level(self, level):
        self._level = level

    @property
    def width(self):
        return self._width

    @property
    def parent(self):
        return self._parent

    @parent.setter
    def parent(self, parent):
        self._parent = parent

    @property
    def ppc(self):
        return self._ppc

    # -- Methods ---------------- --- --  -

    def enable(self, level=2):
        self._level = level
        return self

    def disable(self):
        self._level = 0
        return self

    @contextmanager
    def indent(self):
        if self.info_enabled:
            prev_indent = self._indent
            self._indent += 1
            try:
                with self._ppc.indent():
                    yield
            finally:
                self._indent = prev_indent
        else:
            try:
                yield
            finally:
                pass

    @contextmanager
    def debug_indent(self):
        if self.debug_enabled:
            prev_indent = self._indent
            self._indent += 1
            try:
                with self._ppc.indent():
                    yield
            finally:
                self._indent = prev_indent
        else:
            try:
                yield
            finally:
                pass

    @contextmanager
    def trace_indent(self):
        if self.trace_enabled:
            prev_indent = self._indent
            self._indent += 1
            try:
                with self._ppc.indent():
                    yield
            finally:
                self._indent = prev_indent
        else:
            try:
                yield
            finally:
                pass

    def indent_once(self, to=None):
        self._indent = to or self._indent + 1
        self._ppc.indentation += self._ppc.default_indent

    def dedent(self):
        self._indent = max(self._indent - 1, 0)
        new_indent_len = max(0, (len(self._ppc.indentation) -
                                 len(self._ppc.default_indent)))
        self._ppc.indentation = self._ppc.indentation[:new_indent_len]
        return self

    def debug(self,
              *msgs,
              bullet=None,
              indent="",
              key_style=None,
              margin=0,
              style=None,
              truncate=None):
        if style is None:
            style = PPStyles.grey_3
        self.log(*msgs,
                 bullet=bullet,
                 indent=indent,
                 key_style=key_style,
                 level=Logger.DEBUG,
                 margin=margin,
                 style=style,
                 truncate=truncate)

    def trace(self,
              *msgs,
              bullet=None,
              indent="",
              key_style=None,
              margin=0,
              style=None,
              truncate=None):
        if style is None:
            style = PPStyles.grey_4
        self.log(*msgs,
                 bullet=bullet,
                 indent=indent,
                 key_style=key_style,
                 level=Logger.TRACE,
                 margin=margin,
                 style=style,
                 truncate=truncate)

    def info(self,
             *msgs,
             bullet=None,
             indent="",
             key_style=None,
             margin=0,
             style=None,
             truncate=None):
        self.log(*msgs,
                 bullet=bullet,
                 indent=indent,
                 key_style=key_style,
                 level=Logger.INFO,
                 margin=margin,
                 style=style,
                 truncate=truncate)

    def log(self,
            *msgs,
            bullet=None,
            indent="",
            key_style=None,
            level=TRACE,
            margin=0,
            style=None,
            truncate=None):
        if 0 < self._level <= level:
            self.handle_log(*msgs,
                            bullet=bullet,
                            indent=indent,
                            key_style=key_style,
                            level=level,
                            margin=margin,
                            style=style,
                            truncate=truncate)

    def reset(self):
        """Resets the LOGGER, i.e. resets indentation to 0."""
        self._indent = 0
        self._ppc.indentation = ""

    # noinspection PyShadowingBuiltins
    def log_connectum(self,
                      cnm,
                      *,
                      all=False,
                      bindings=False,
                      binding_sources=False,
                      checked=False,
                      history=False,
                      label=None,
                      level=DEBUG,
                      resolve_state=True,
                      sub_connecta=True,
                      truncate=0) -> None:
        raise NotImplementedError()


class VoidLogger(LoggerBase):
    """A logger that does nothing."""

    def debug(self,
              *msgs,
              bullet=None,
              indent="",
              key_style=None,
              level=LoggerBase.TRACE,
              margin=0,
              style=None,
              truncate=None):
        pass

    def trace(self,
              *msgs,
              bullet=None,
              indent="",
              key_style=None,
              level=LoggerBase.TRACE,
              margin=0,
              style=None,
              truncate=None):
        pass

    def info(self,
             *msgs,
             bullet=None,
             indent="",
             key_style=None,
             level=LoggerBase.TRACE,
             margin=0,
             style=None,
             truncate=None):
        pass

    def log(self,
            *msgs,
            bullet=None,
            indent="",
            key_style=None,
            level=LoggerBase.TRACE,
            margin=0,
            style=None,
            truncate=None):
        pass

    def handle_log(self,
                   *msgs,
                   bullet=None,
                   indent="",
                   key_style=None,
                   level=LoggerBase.TRACE,
                   margin=0,
                   style=None,
                   truncate=None):
        pass

    # noinspection PyShadowingBuiltins
    def log_connectum(self,
                      cnm,
                      *,
                      all=False,
                      bindings=False,
                      binding_sources=False,
                      checked=False,
                      history=False,
                      label=None,
                      level=LoggerBase.DEBUG,
                      resolve_state=True,
                      sub_connecta=True,
                      truncate=0):
        pass


Logger.Void = VoidLogger()
LoggerBase.Void = VoidLogger()
