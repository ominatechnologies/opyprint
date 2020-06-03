from __future__ import annotations

import abc
from contextlib import contextmanager
from typing import ClassVar, Optional

from ..pp_context import PPContext
from ..pp_styles import PPStyles
from ..typing import StyleOptions


class Logger:
    """Abstract base class for concrete Logger classes."""

    # -- Class Vars and Methods ---------------- --- --  -

    DISABLED: ClassVar[int] = 0
    DEBUG: ClassVar[int] = 1
    TRACE: ClassVar[int] = 2
    INFO: ClassVar[int] = 3

    Void: ClassVar[Logger]

    # -- Instance Initialization ---------------- --- --  -

    __slots__ = (
        '_indent',
        '_level',
        '_log_history',
        '_log_resolve_state',
        '_parent',
        '_ppc',
        '_width',
    )

    _indent: int
    _level: int
    _ppc: PPContext
    _width: int

    def __init__(self,
                 level: int = 2,
                 log_history: bool = False,
                 log_resolve_state: bool = True,
                 width: int = 100,
                 parent: Logger = None):
        """

        :param level: log level
        :param log_history: See 'log_connectum' method.
        :param log_resolve_state: See 'log_connectum' method.
        :param width: max content width
        :param parent: When given, the indentation of this parent logger is
            added to the indentation of this "dependent" logger.
        """
        self._indent = 0
        self._level = level
        self._log_history = log_history
        self._log_resolve_state = log_resolve_state
        self._parent = parent
        self._ppc = PPContext(width=width)
        self._width = width

    # -- Accessors ---------------- --- --  -

    @property
    def enabled(self) -> bool:
        """
        True when the logger is enabled, i.e. when the log level is not 0.
        """
        return self._level > 0

    @property
    def debug_enabled(self) -> bool:
        """True when the 'debug' log level is enabled."""
        return 0 < self._level <= Logger.DEBUG

    @property
    def trace_enabled(self) -> bool:
        """True when the 'trace' log level is enabled."""
        return 0 < self._level <= Logger.TRACE

    @property
    def info_enabled(self) -> bool:
        """True when the 'info' log level is enabled."""
        return 0 < self._level <= Logger.INFO

    @property
    def disabled(self) -> bool:
        """
        True when the logger is disabled, i.e. when the log level is 0.
        """
        return self._level == 0

    @property
    def indent_depth(self) -> int:
        if self._parent:
            return self._parent.indent_depth + self._indent
        else:
            return self._indent

    @property
    def indentation(self) -> str:
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
    def width(self) -> int:
        return self._width

    @property
    def parent(self) -> Optional[Logger]:
        return self._parent

    @parent.setter
    def parent(self, parent: Logger):
        self._parent = parent

    @property
    def ppc(self) -> PPContext:
        return self._ppc

    # -- Abstract Methods ---------------- --- --  -

    @abc.abstractmethod
    def handle_log(self,
                   *msgs,
                   bullet: str = None,
                   indent: str = "",
                   key_style: StyleOptions = None,
                   level: int = TRACE,
                   margin: int = 0,
                   style: StyleOptions = None) -> None:
        """
        Handle a log message.

        :param msgs: The messages.
        :param bullet: Optional bullet.
        :param indent: The indentation prefix string.
        :param key_style: Optional style specifications for the key part of
            key-value pairs.
        :param level: Optional log level.
        :param margin: Optional margin.
        :param style: Optional styling.
        """
        pass

    # -- Methods ---------------- --- --  -

    def enable(self, level: int = 2) -> Logger:
        """Enable the LOGGER and set the given log level (default: 'trade')."""
        self._level = level
        return self

    def disable(self) -> Logger:
        """Disable the LOGGER."""
        self._level = 0
        return self

    @contextmanager
    def indent(self):
        """Increase the indentation for the subsequent log calls."""
        prev_indent = self._indent
        self._indent += 1
        try:
            with self._ppc.indent():
                yield
        finally:
            self._indent = prev_indent

    def indent_once(self, to: int = None):
        """Increase the indentation for the subsequent log calls."""
        self._indent = to or self._indent + 1
        self._ppc.indentation += self._ppc.default_indent

    def dedent(self):
        """Decrease the indentation for the subsequent log calls."""
        self._indent = max(self._indent - 1, 0)
        new_indent_len = max(0, (len(self._ppc.indentation) -
                                 len(self._ppc.default_indent)))
        self._ppc.indentation = self._ppc.indentation[:new_indent_len]
        return self

    def debug(self,
              *msgs,
              bullet: str = None,
              indent: str = "",
              key_style: StyleOptions = None,
              margin: int = 0,
              style: StyleOptions = None) -> None:
        """
        Log at level 1.

        :param msgs: The messages.
        :param bullet: Optional bullet.
        :param indent: The indentation prefix string.
        :param key_style: Optional style specifications for the key part of
            key-value pairs.
        :param margin: Optional margin.
        :param style: Optional styling.
        """
        if style is None:
            style = PPStyles.grey_3
        self.log(*msgs,
                 bullet=bullet,
                 indent=indent,
                 key_style=key_style,
                 level=Logger.DEBUG,
                 margin=margin,
                 style=style)

    def trace(self,
              *msgs,
              bullet: str = None,
              indent: str = "",
              key_style: StyleOptions = None,
              margin: int = 0,
              style: StyleOptions = None) -> None:
        """
        Log at level 2.

        :param msgs: The messages.
        :param bullet: Optional bullet.
        :param indent: The indentation prefix string.
        :param key_style: Optional style specifications for the key part of
            key-value pairs.
        :param margin: Optional margin.
        :param style: Optional styling.
        """
        if style is None:
            style = PPStyles.grey_4
        self.log(*msgs,
                 bullet=bullet,
                 indent=indent,
                 key_style=key_style,
                 level=Logger.TRACE,
                 margin=margin,
                 style=style)

    def info(self,
             *msgs,
             bullet: str = None,
             indent: str = "",
             key_style: StyleOptions = None,
             margin: int = 0,
             style: StyleOptions = None) -> None:
        """
        Log at level 3.

        :param msgs: The messages.
        :param bullet: Optional bullet.
        :param indent: The indentation prefix string.
        :param key_style: Optional style specifications for the key part of
            key-value pairs.
        :param margin: Optional margin.
        :param style: Optional styling.
        """
        self.log(*msgs,
                 bullet=bullet,
                 indent=indent,
                 key_style=key_style,
                 level=Logger.INFO,
                 margin=margin,
                 style=style)

    def log(self,
            *msgs,
            bullet: str = None,
            indent: str = "",
            key_style: StyleOptions = None,
            level: int = TRACE,
            margin: int = 0,
            style: StyleOptions = None) -> None:
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
        """
        if 0 < self._level <= level:
            self.handle_log(*msgs,
                            bullet=bullet,
                            indent=indent,
                            key_style=key_style,
                            level=level,
                            margin=margin,
                            style=style)

    def reset(self) -> None:
        """Resets the LOGGER, i.e. resets indentation to 0."""
        self._indent = 0
        self._ppc.indentation = ""
