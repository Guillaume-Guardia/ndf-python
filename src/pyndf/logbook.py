# -*- coding: utf-8 -*-

from time import time
import logging

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s.%(msecs)03d] [%(levelname)s] %(name)s: %(message)s",
    datefmt="%d-%b-%y %H:%M:%S",
)


class Logger:
    """Log class"""

    def __init__(self, *args, **kwargs):
        """Initialisation method"""
        super().__init__(*args, **kwargs)
        self.log = logging.getLogger(self.__class__.__name__)


def log_time(func):
    """Log time function.

    Args:
        func (method): wrapped function.

    Returns:
        ?: result of the wrapped function.
    """
    log = logging.getLogger("Time")

    def wrapper(*args, **kwargs):
        start = time()
        log.info(f"START {func.__name__}")
        result = func(*args, **kwargs)
        log.info(f"END {time() - start}")
        return result

    return wrapper
