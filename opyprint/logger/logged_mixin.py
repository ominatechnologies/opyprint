from __future__ import annotations

from contextlib import contextmanager
from typing import Generic, TypeVar

from .logger import Logger
from ..typing import StyleOptions

T = TypeVar("T", bound=Logger)


class LoggedMixin(Generic[T]):
    _logger: T

    def __init__(self, logger: T):
        self._logger = logger
        super().__init__()

    # -- Logger Methods --------------- --- --  -

    @property
    def logger(self) -> T:
        return self._logger

    @logger.setter
    def logger(self, logger: T) -> None:
        self._logger = logger

    @property
    def debug_enabled(self) -> bool:
        return self._logger.debug_enabled

    @property
    def trace_enabled(self) -> bool:
        return self._logger.trace_enabled

    @property
    def info_enabled(self) -> bool:
        return self._logger.info_enabled

    def debug(self,
              *msgs,
              bullet: str = None,
              indent: str = "",
              key_style: StyleOptions = None,
              margin: int = 0,
              style: StyleOptions = None):
        self._logger.debug(*msgs,
                           bullet=bullet,
                           indent=indent,
                           key_style=key_style,
                           margin=margin,
                           style=style)

    def trace(self,
              *msgs,
              bullet: str = None,
              indent: str = "",
              key_style: StyleOptions = None,
              margin: int = 0,
              style: StyleOptions = None):
        self._logger.trace(*msgs,
                           bullet=bullet,
                           indent=indent,
                           key_style=key_style,
                           margin=margin,
                           style=style)

    def info(self,
             *msgs,
             bullet: str = None,
             indent: str = "",
             key_style: StyleOptions = None,
             margin: int = 0,
             style: StyleOptions = None):
        self._logger.info(*msgs,
                          bullet=bullet,
                          indent=indent,
                          key_style=key_style,
                          margin=margin,
                          style=style)

    @contextmanager
    def indent(self):
        """
        Increase the indentation for the subsequent log calls if the log level
        is info or higher.
        """
        try:
            if self._logger.info_enabled:
                with self._logger.indent():
                    yield
            else:
                yield
        finally:
            pass

    @contextmanager
    def debug_indent(self):
        """
        Increase the indentation for the subsequent log calls if the log level
        is debug or higher.
        """
        try:
            if self._logger.debug_enabled:
                with self._logger.indent():
                    yield
            else:
                yield
        finally:
            pass

    @contextmanager
    def trace_indent(self):
        """
        Increase the indentation for the subsequent log calls if the log level
        is trace or higher.
        """
        try:
            if self._logger.trace_enabled:
                with self._logger.indent():
                    yield
            else:
                yield
        finally:
            pass
