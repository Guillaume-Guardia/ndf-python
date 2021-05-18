# -*- coding: utf-8 -*-

from pyndf.qtlib import QtWidgets


class AbstractTable(QtWidgets.QTableWidget):
    def __init__(self, tab, item):
        super().__init__(tab)
        self.tab = tab

        self.custom_item = item
        self.column_count = item.column_count()

    def init(self):
        self.clear()
        self.setColumnCount(self.column_count)
        self.setRowCount(0)
        self.setHorizontalHeaderLabels(self.custom_item.headers_pretty())

    def add_row(self):
        row = self.rowCount()
        self.insertRow(row)
        return row

    def add(self, obj):
        row = self.add_row()

        for index, (name, widget) in enumerate(obj):
            self.setItem(row, index, widget)

    def finished(self):
        pass
