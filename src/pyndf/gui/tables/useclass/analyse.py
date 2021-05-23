# -*- coding: utf-8 -*-

from pyndf.gui.tables.abstract import AbstractTable
from pyndf.constants import CONST
from pyndf.gui.items.factory import Items


class AnalyseTable(AbstractTable):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # total time
        self.time = 0

    def init(self):
        super().init()
        self.time = 0

    def add(self, obj):
        self.time += float(obj.time.text())
        super().add(obj)

    def finished(self):
        row = self.add_row()

        # Check all status
        total_status = set()
        for r in range(self.rowCount() - 1):
            item = self.item(r, self.custom_item.headers.index("status"))
            status = getattr(CONST.STATUS, item.text())
            total_status.add(status.NAME)
        total_status = "/".join(list(total_status))
        total_item = Items(CONST.TYPE.TOT, total_status, self.time)

        # Set total at the end
        self.setVerticalHeaderItem(row, total_item.vheaders_pretty)

        # Add the value from item
        for name, widget in total_item:
            self.setItem(row, self.custom_item.headers.index(name), widget)
        super().finished()
