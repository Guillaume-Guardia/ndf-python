# -*- coding: utf-8 -*-

from pyndf.constants import CONST
from pyndf.qtlib import QtWidgets, QtCore


class AbstractTable(QtWidgets.QTableWidget):
    sort_order = {True: QtCore.Qt.SortOrder.AscendingOrder, False: QtCore.Qt.SortOrder.DescendingOrder}

    def __init__(self, tab, item, read_only=True):
        super().__init__(tab)
        self.read_only = read_only
        self.tab = tab
        self.custom_item = item
        self.set_horizontal_headers()

        # Header
        self.horizontalHeader().setSortIndicatorShown(True)
        self.horizontalHeader().setSectionsClickable(True)
        self.horizontalHeader().setSectionsMovable(True)
        self.horizontalHeader().sectionClicked.connect(self.on_header_clicked)

        self.__cache = {}

    def set_horizontal_headers(self, headers=None):
        if headers is None:
            headers = self.custom_item.headers_pretty()
        self.setColumnCount(len(headers))
        self.setHorizontalHeaderLabels(headers)
        header = self.horizontalHeader()
        for col in range(self.columnCount()):
            header.setSectionResizeMode(col, QtWidgets.QHeaderView.ResizeMode.ResizeToContents)

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

        # get dev mode from menu of main window
        dev_mode = False
        if self.tab.window.menuWidget():
            dev_mode = self.tab.window.menuWidget()._actions[CONST.TYPE.DEV_MODE].isChecked()

        for column, (name, widget) in enumerate(obj):
            try:
                widget.update_mode(dev_mode)
                self.setItem(row, column, widget)
                if self.read_only:
                    widget.setFlags(QtCore.Qt.ItemFlag.ItemIsEnabled)
            except TypeError:
                if name == "filename":
                    # Add item behind the button for the research in table
                    self.setItem(row, column, QtWidgets.QTableWidgetItem(widget.path))
                self.setCellWidget(row, column, widget)
        return widget

    def finished(self, boolean=True):
        if self.tab.window.menuWidget() is not None:
            self.tab.window.menuWidget()._actions[self.custom_item.type].setChecked(boolean)
        else:
            self.tab.window.toggled_tab(self.tab, boolean)

    def on_header_clicked(self, col):
        if col in self.__cache:
            self.__cache[col] = not self.__cache[col]
        else:
            self.__cache[col] = True
        sort = self.sort_order[self.__cache[col]]
        self.sortItems(col, sort)
