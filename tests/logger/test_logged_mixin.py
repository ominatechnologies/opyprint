# test_logged_mixin

from typing import Dict

from opyprint import print  # noqa: F401
from opyprint.logger import Logger, LoggedMixin, PrintLogger


def test_1():
    class Target(LoggedMixin):
        __slots__ = ["_logger"]

        def __init__(self, log_level: int = Logger.DISABLED):
            LoggedMixin.__init__(self, PrintLogger(log_level))

    obj = Target(log_level=PrintLogger.INFO)

    assert isinstance(obj.logger, PrintLogger)
    assert obj.logger.level == PrintLogger.INFO


def test_2():
    class Base:
        __slots__ = ["config"]

        config: Dict

        def __init__(self, config: Dict):
            self.config = config

    class Target(Base, LoggedMixin):
        __slots__ = ["_logger"]

        def __init__(self,
                     config: Dict,
                     log_level: int = Logger.DISABLED):
            Base.__init__(self, config)
            LoggedMixin.__init__(self, PrintLogger(log_level))

    obj = Target(config={"k_1": "v_1"}, log_level=PrintLogger.INFO)

    assert isinstance(obj.logger, PrintLogger)
    assert obj.logger.level == PrintLogger.INFO
