# -*- coding: utf-8 -*-

from pyndf.qtlib import QtWidgets
from pyndf.constants import CONFIG
from pyndf.gui.items.total_item import TotalItem


class AnalyseTable(QtWidgets.QTableWidget):
    def __init__(self, tab, item):
        super().__init__(tab)
        self.tab = tab

        self.custom_item = item
        self.column_count = item.column_count()

        # total time
        self.time = 0

    def init(self):
        self.clear()
        self.time = 0
        self.setColumnCount(self.column_count)
        self.setRowCount(0)
        self.setHorizontalHeaderLabels(self.custom_item.headers_pretty())

    def add_row(self):
        row = self.rowCount()
        self.insertRow(row)
        return row

    def add(self, obj):
        row = self.add_row()

        self.time += float(obj.time.text())
        for index, (name, widget) in enumerate(obj):
            self.setItem(row, index, widget)

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
