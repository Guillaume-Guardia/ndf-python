# -*- coding: utf-8 -*-

from pyndf.gui.tables.abstract import AbstractTable
from pyndf.constants import CONST
from pyndf.gui.items.factory import Items
from pyndf.utils import Utils


class AnalyseTable(AbstractTable):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # total time
        self.time = 0

    def init(self, *args, **kwargs):
        super().init(*args, **kwargs)
        self.time = 0

    def add(self, obj):
        self.time += float(obj.time.text())

        last_item = super().add(obj)
        if not CONST.OPTI:
            self.scrollToItem(last_item)

    def finished(self):
        row = self.add_row()

        # Check all status
        total_status = set()
        for r in range(self.rowCount() - 1):
            status = self.item(r, self.custom_item.headers.index("status")).text()
            if status:
                total_status.add(status)

        # Create total item
        total_item = Items(CONST.TYPE.TOT, Utils.getattr(CONST.STATUS, total_status), self.time)

        # Set total at the end
        self.setVerticalHeaderItem(row, total_item.vheaders_pretty)

        # Add the value from item
        for name, widget in total_item:
            self.setItem(row, self.custom_item.headers.index(name), widget)
        super().finished()
