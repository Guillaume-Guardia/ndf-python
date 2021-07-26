# -*- coding: utf-8 -*-

from pyndf.constants import CONST
from pyndf.gui.items.abstract import AbstractItem


class ExcelItem(AbstractItem):
    """Class for storing data for analyse."""

    type = CONST.TYPE.EXC

    def __init__(self, *args, filename=None, **kwargs):
        """Initialisation"""
        super().__init__(*args, **kwargs)
        self.filename = filename

    @classmethod
    def headers_pretty(cls):
        # headers
        return cls.headers
