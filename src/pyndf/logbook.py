# -*- coding: utf-8 -*-

from time import time
import logging
from colorlog import ColoredFormatter


class Logger:
    """Log class"""

    def __init__(self, *args, **kwargs):
        """Initialisation method"""
        super().__init__(*args, **kwargs)
        self.log_level = logging.INFO
        self.log = self.setup_logger()

    def setup_logger(self):
        """Return a logger with a default ColoredFormatter."""
        formatter = ColoredFormatter(
            "%(log_color)s[%(asctime)s.%(msecs)03d][%(levelname)-8s] %(name)-20s: %(reset)s%(white)s%(message)s",
            datefmt="%d-%b-%y %H:%M:%S",
            reset=True,
            log_colors={
                "DEBUG": "cyan",
                "INFO": "green",
                "WARNING": "yellow",
                "ERROR": "red",
                "CRITICAL": "red",
            },
        )

        logger = logging.getLogger(self.__class__.__name__)
        logger.setLevel(self.log_level)

        if len(logger.handlers) == 0:
            handler = logging.StreamHandler()
            handler.setFormatter(formatter)
            logger.addHandler(handler)

        return logger


def log_time(func):
    """Log time function.

    Args:
        func (method): wrapped function.

    Returns:
        ?: result of the wrapped function.
    """

    def wrapper(*args, **kwargs):
        start = time()
        args[0].log.info(f"START {func.__name__}")
        result = func(*args, **kwargs)
        args[0].log.info(f"END {func.__name__} {round(time() - start, 5)} .")
        return result

    return wrapper
