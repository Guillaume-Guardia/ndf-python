# -*- coding: utf-8 -*-

from pyndf.qtlib import QtWidgets, QtCore


class AbstractTable(QtWidgets.QTableWidget):
    _cache = {}

    sort_order = {True: QtCore.Qt.SortOrder.AscendingOrder, False: QtCore.Qt.SortOrder.DescendingOrder}

    def __init__(self, tab, item):
        super().__init__(tab)
        self.tab = tab
        self.custom_item = item
        self.set_horizontal_headers()

    def set_horizontal_headers(self, headers=None):
        if headers is None:
            headers = self.custom_item.headers_pretty()
        self.setColumnCount(len(headers))
        self.setHorizontalHeaderLabels(headers)
        header = self.horizontalHeader()
        for col in range(self.columnCount()):
            header.setSectionResizeMode(col, QtWidgets.QHeaderView.ResizeMode.ResizeToContents)

        header.setSortIndicatorShown(True)
        header.setSectionsClickable(True)
        header.setSectionsMovable(True)
        header.sectionClicked.connect(self.on_header_clicked)

    def init(self, clear=True, matricule=None):
        if matricule is not None:
            # Remove all row which refer to the specific matricule
            rows_to_delete = []

            for row in range(self.rowCount()):
                try:
                    column = self.custom_item.headers.index("matricule")
                    if self.item(row, column).data(QtCore.Qt.ItemDataRole.EditRole) != matricule:
                        continue
                except (ValueError, AttributeError):
                    pass
                rows_to_delete.append(row)

            rows_to_delete.reverse()
            for row in rows_to_delete:
                self.removeRow(row)
            return

        if clear:
            # Remove all rows
            self.clearContents()
            self.setRowCount(0)

    def add_row(self):
        row = self.rowCount()
        self.insertRow(row)
        return row

    def add_column(self):
        col = self.columnCount()
        self.insertColumn(col)
        return col

    def add(self, obj):
        row = self.add_row()

        if self.columnCount() != obj.counter:
            self.set_horizontal_headers(obj.headers)
            self.custom_item.headers = obj.headers

        for column, (name, widget) in enumerate(obj):
            try:
                self.setItem(row, column, widget)
            except TypeError:
                self.setCellWidget(row, column, widget)
        return widget

    def finished(self, boolean=True):
        if self.tab.window.menuWidget() is not None:
            self.tab.window.menuWidget()._actions[self.custom_item.type].setChecked(boolean)
        else:
            self.tab.window.toggled_tab(self.tab, boolean)

    def on_header_clicked(self, col):
        if col in self._cache:
            self._cache[col] = not self._cache[col]
        else:
            self._cache[col] = False
        sort = self.sort_order[self._cache[col]]
        self.sortItems(col, sort)
