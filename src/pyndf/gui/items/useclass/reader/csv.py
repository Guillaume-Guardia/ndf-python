# -*- coding: utf-8 -*-

from pyndf.constants import CONFIG, COL_CSV
from pyndf.gui.items.abstract import AbstractItem


class CsvItem(AbstractItem):
    """Class for storing data for analyse."""

    headers = list(CONFIG[COL_CSV].values())

    @classmethod
    def headers_pretty(cls):
        # headers
        return cls.headers
