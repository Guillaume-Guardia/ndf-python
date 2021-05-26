# -*- coding: utf-8 -*-

from pyndf.constants import CONST
from pyndf.gui.items.abstract import AbstractItem


class ExcelItem(AbstractItem):
    """Class for storing data for analyse."""

    type = CONST.TYPE.EXC

    @classmethod
    def headers_pretty(cls):
        # headers
        return cls.headers
