from __future__ import annotations

from .logger import Logger


class PrintLogger(Logger):
    """Logger that simply prints to stdout."""

    def handle_log(self,
                   *msgs,
                   bullet=None,
                   indent="",
                   key_style=None,
                   level=Logger.TRACE,
                   margin=0,
                   style=None):
        if margin:
            for i in range(margin):
                self.ppc.newline()

        if self.parent:
            indent += self.parent.indentation
        if indent:
            with self.ppc.indent(indent):
                self.ppc(*msgs,
                         bullet=bullet,
                         key_style=key_style,
                         style=style)
        else:
            self.ppc(*msgs, bullet=bullet, key_style=key_style, style=style)

        if margin:
            for i in range(margin):
                self.ppc.newline()

        self.ppc.print()
