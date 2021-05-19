# -*- coding: utf-8 -*-

from pyndf.gui.items.abstract import AbstractItem


class AllItem(AbstractItem):
    """Class for storing data for analyse."""

    headers = ["name", "status", "time"]

    @classmethod
    def headers_pretty(cls):
        # headers
        return [cls.tr("Process name"), cls.tr("Status"), cls.tr("Time (s)")]
