# -*- coding: utf-8 -*-

from pyndf.gui.items.abstract import AbstractItem
from pyndf.constants import CONST


class AllItem(AbstractItem):
    """Class for storing data for analyse."""

    type = CONST.TYPE.ALL

    @classmethod
    def headers_pretty(cls):
        # headers
        return [cls.tr("Process name"), cls.tr("Status"), cls.tr("Time (s)")]
