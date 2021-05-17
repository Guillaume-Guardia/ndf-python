# -*- coding: utf-8 -*-

from pyndf.gui.items.item import Item


class TotalItem(Item):
    """Class for storing data for analyse."""

    headers = ["status", "time"]
    vheaders = ["total"]

    def __init__(self, status, time):
        """Initialisation"""
        super().__init__()
        self.status = "OK" if status else "NO"
        self.time = time
        self.vheaders_pretty = self.tr("Total")
