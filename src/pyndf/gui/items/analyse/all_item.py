# -*- coding: utf-8 -*-

from pyndf.gui.items.item import Item


class AllItem(Item):
    """Class for storing data for analyse."""

    headers = ["name", "status", "time"]

    @classmethod
    def headers_pretty(cls):
        # headers
        return [cls.tr("Process name"), cls.tr("Status"), cls.tr("Time (s)")]
