# -*- coding: utf-8 -*-

from pyndf.gui.tables.abstract import AbstractTable
from pyndf.constants import CONFIG
from pyndf.gui.items.analyse.total_item import TotalItem


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

        status = all(
            [
                self.item(r, self.custom_item.headers.index("status")).text() in CONFIG["good_status"]
                for r in range(self.rowCount() - 1)
            ]
        )
        total_item = TotalItem(status, self.time)

        self.setVerticalHeaderItem(row, total_item.vheaders_pretty)

        for name, widget in total_item:
            self.setItem(row, self.custom_item.headers.index(name), widget)
