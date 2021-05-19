# -*- coding: utf-8 -*-

from pyndf.gui.tables.abstract import AbstractTable
from pyndf.constants import CONFIG
from pyndf.gui.items.useclass.analyse.total import TotalItem


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
        status = all(
            [
                self.item(r, self.custom_item.headers.index("status")).text() in CONFIG["good_status"]
                for r in range(self.rowCount() - 1)
            ]
        )
        total_item = TotalItem(status, self.time)

        # Set total at the end
        self.setVerticalHeaderItem(row, total_item.vheaders_pretty)

        # Add the value from item
        for name, widget in total_item:
            self.setItem(row, self.custom_item.headers.index(name), widget)
        super().finished()