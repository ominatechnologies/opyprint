from __future__ import annotations

from abc import ABC

from .logger import LoggerBase


class PrintLogger(LoggerBase, ABC):
    """Logger that simply prints to stdout."""

    def handle_log(self,
                   *msgs,
                   bullet=None,
                   indent="",
                   key_style=None,
                   level=LoggerBase.TRACE,
                   margin=0,
                   style=None,
                   truncate=None):
        if margin:
            for i in range(margin):
                self.ppc.newline()

        if self.parent:
            indent += self.parent.indentation

        self.ppc(*msgs,
                 bullet=bullet,
                 indent=indent,
                 key_style=key_style,
                 style=style,
                 truncate=truncate)

        if margin:
            for i in range(margin):
                self.ppc.newline()

        self.ppc.print()
