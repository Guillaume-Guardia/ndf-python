# -*- coding: utf-8 -*-

from PyQt6 import QtWidgets


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
        self.table.clear()
        self.table.setColumnCount(len(self.headers))
        self.table.setHorizontalHeaderLabels(self.headers)
        self.table.setRowCount(0)

    def analysed(self, obj):
        row_count = self.table.rowCount()
        self.table.insertRow(row_count)

        self.time_counter += obj.time
        for index, attribute in enumerate(self.headers):
            self.table.setItem(row_count, index, QtWidgets.QTableWidgetItem(str(getattr(obj, attribute))))

    def finished(self):
        row_count = self.table.rowCount()
        self.table.insertRow(row_count)
        self.table.setVerticalHeaderItem(row_count, QtWidgets.QTableWidgetItem(self.tr("Total")))
        col_count = self.table.columnCount()
        self.table.setItem(row_count, col_count - 1, QtWidgets.QTableWidgetItem(str(round(self.time_counter, 2))))
        self.show()
