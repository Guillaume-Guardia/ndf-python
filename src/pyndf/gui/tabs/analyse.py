# -*- coding: utf-8 -*-

from pyndf.qtlib import QtWidgets
from pyndf.gui.tables.factory import tables_factory


class AnalyseTab(QtWidgets.QWidget):
    def __init__(self, window, title, item):
        super().__init__()
        self.window = window
        self.title = title

        # Create table
        self.table = tables_factory(self, item)

        # Add table
        layout = QtWidgets.QHBoxLayout()
        layout.addWidget(self.table)
        self.setLayout(layout)
