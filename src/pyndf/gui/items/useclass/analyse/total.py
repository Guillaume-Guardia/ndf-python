# -*- coding: utf-8 -*-

from pyndf.gui.items.abstract import AbstractItem
from pyndf.constants import CONST


class TotalItem(AbstractItem):
    """Class for storing data for analyse."""

    type = CONST.TYPE.TOT
    headers = ["status", "time"]
    vheaders = ["total"]

    def __init__(self, status, time):
        """Initialisation"""
        super().__init__()
        self.status = "OK" if status else "NO"
        self.time = time
        self.vheaders_pretty = self.tr("Total")
