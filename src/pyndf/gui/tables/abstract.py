# -*- coding: utf-8 -*-

from pyndf.qtlib import QtWidgets


class AbstractTable(QtWidgets.QTableWidget):
    def __init__(self, tab, item):
        super().__init__(tab)
        self.tab = tab

        self.custom_item = item

        headers = self.custom_item.headers_pretty()
        self.setColumnCount(len(headers))
        self.setHorizontalHeaderLabels(headers)

    def init(self):
        self.clearContents()
        self.setRowCount(0)

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
