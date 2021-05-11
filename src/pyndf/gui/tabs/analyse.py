# -*- coding: utf-8 -*-

from PyQt6 import QtWidgets, QtGui
from pyndf.constants import CONFIG, COLORS


class AnalyseTab(QtWidgets.QWidget):
    def __init__(self, window, title, item):
        super().__init__()
        self.window = window
        self.title = title

        # Create table
        self.headers = item.headers()
        self.table = QtWidgets.QTableWidget()

        # Add table
        layout = QtWidgets.QHBoxLayout()
        layout.addWidget(self.table)
        self.setLayout(layout)

        # Time counter
        self.time_counter = 0

    def init_table(self):
        self.time_counter = 0
        self.table.clear()
        self.table.setColumnCount(len(self.headers))
        self.table.setHorizontalHeaderLabels(self.headers)
        self.table.setRowCount(0)

    def analysed(self, obj):
        row = self.table.rowCount()
        self.table.insertRow(row)

        self.time_counter += obj.time
        for index, attribute in enumerate(self.headers):
            attr = getattr(obj, attribute)
            if isinstance(attr, float):
                attr = round(attr, 2)
            self.table.setItem(row, index, QtWidgets.QTableWidgetItem(str(attr)))

        # Set Color indicator
        self.set_color_row(row, COLORS.get(obj.status, COLORS["others"]))

    def finished(self):
        row_count = self.table.rowCount()
        self.table.insertRow(row_count)
        self.table.setVerticalHeaderItem(row_count, QtWidgets.QTableWidgetItem(self.tr("Total")))
        col_count = self.table.columnCount()
        self.table.setItem(row_count, col_count - 1, QtWidgets.QTableWidgetItem(str(round(self.time_counter, 2))))

        # Check is all are ok
        check = all(
            [
                self.table.item(row, col_count - 2).text() in CONFIG["good_status"]
                for row in range(self.table.rowCount() - 1)
            ]
        )

        if check:
            self.table.setItem(row_count, col_count - 2, QtWidgets.QTableWidgetItem(CONFIG["good_status"][0]))
            self.set_color_row(row_count, COLORS[CONFIG["good_status"][0]])

    def set_color_row(self, rowIndex, color):
        for j in range(self.table.columnCount()):
            try:
                self.table.item(rowIndex, j).setBackground(QtGui.QColor(color))
            except AttributeError:
                pass
