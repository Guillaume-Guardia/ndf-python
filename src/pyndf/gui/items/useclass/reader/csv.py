# -*- coding: utf-8 -*-

from pyndf.constants import CONST
from pyndf.gui.items.abstract import AbstractItem


class CsvItem(AbstractItem):
    """Class for storing data for analyse."""

    type = CONST.TYPE.CSV
    headers = list(CONST.FILE.YAML[CONST.TYPE.CSV].values())

    @classmethod
    def headers_pretty(cls):
        # headers
        return cls.headers
