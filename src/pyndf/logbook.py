#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging

logging.basicConfig(
    level=logging.DEBUG, format="[%(asctime)-15s] [%(levelname)s] %(name)s: %(message)s", datefmt="%d-%b-%y %H:%M:%S"
)


class Logger:
    def __init__(self):
        self.log = logging.getLogger(self.__class__.__name__)
