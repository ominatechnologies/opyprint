from __future__ import annotations

from .logger import Logger


class VoidLogger(Logger):
    """A logger that does nothing."""

    def debug(self,
              *msgs,
              bullet=None,
              indent="",
              key_style=None,
              level=Logger.TRACE,
              margin=0,
              style=None):
        pass

    def trace(self,
              *msgs,
              bullet=None,
              indent="",
              key_style=None,
              level=Logger.TRACE,
              margin=0,
              style=None):
        pass

    def info(self,
             *msgs,
             bullet=None,
             indent="",
             key_style=None,
             level=Logger.TRACE,
             margin=0,
             style=None):
        pass

    def log(self,
            *msgs,
            bullet=None,
            indent="",
            key_style=None,
            level=Logger.TRACE,
            margin=0,
            style=None):
        pass

    def handle_log(self,
                   *msgs,
                   bullet=None,
                   indent="",
                   key_style=None,
                   level=Logger.TRACE,
                   margin=0,
                   style=None):
        pass


Logger.Void = VoidLogger()
