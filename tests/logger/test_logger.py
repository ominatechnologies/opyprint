# test_logger

from opyprint import print  # noqa: F401
from opyprint.logger import Logger, LoggerBase, PrintLogger


def test_base_logger():
    assert Logger.DEBUG == LoggerBase.DEBUG
    assert Logger.DISABLED == LoggerBase.DISABLED
    assert Logger.TRACE == LoggerBase.TRACE
    assert Logger.INFO == LoggerBase.INFO


def test_print_logger():
    assert LoggerBase.DEBUG == PrintLogger.DEBUG
    assert LoggerBase.DISABLED == PrintLogger.DISABLED
    assert LoggerBase.TRACE == PrintLogger.TRACE
    assert LoggerBase.INFO == PrintLogger.INFO

    logger = PrintLogger(PrintLogger.INFO)

    assert isinstance(logger, LoggerBase)
    assert isinstance(logger, Logger)

    assert logger.level == PrintLogger.INFO

    # logger.debug("test-msg")
