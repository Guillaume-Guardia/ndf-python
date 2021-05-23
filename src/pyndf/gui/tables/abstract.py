# -*- coding: utf-8 -*-

from pyndf.qtlib import QtWidgets, QtCore


class AbstractTable(QtWidgets.QTableWidget):
    _cache = {}

    sort_order = {True: QtCore.Qt.SortOrder.AscendingOrder, False: QtCore.Qt.SortOrder.DescendingOrder}

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
        self.cellClicked.connect(self.on_header_clicked)
        self.tab.window.toggled_tab(self.tab, True)

    def on_header_clicked(self, row, col):
        if col in self._cache:
            self._cache[col] = not self._cache[col]
        else:
            self._cache[col] = True
        sort = self.sort_order[self._cache[col]]
        self.sortItems(col, sort)
