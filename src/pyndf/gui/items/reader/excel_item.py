# -*- coding: utf-8 -*-

from pyndf.constants import CONFIG, COL
from pyndf.gui.items.item import Item


class ExcelItem(Item):
    """Class for storing data for analyse."""

    headers = list(CONFIG[COL].values())

    @classmethod
    def headers_pretty(cls):
        # headers
        return cls.headers
