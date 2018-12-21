import logging
import sys

LOG_ENTRY_FORMAT = logging.Formatter('%(asctime)s: %(name)s [%(levelname)s] — %(message)s')
LOG_FILENAME = 'rox.log'
LOGGING_LEVEL = logging.DEBUG


def _handler_stdout():
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(LOG_ENTRY_FORMAT)
    return handler


def _handler_file():
    handler = logging.FileHandler(LOG_FILENAME)
    handler.setFormatter(LOG_ENTRY_FORMAT)
    return handler


def get_logger(logger_name):
    logger = logging.getLogger(logger_name)
    logger.setLevel(LOGGING_LEVEL)
    logger.addHandler(_handler_file())
    logger.addHandler(_handler_stdout())
    logger.propagate = False
    return logger
