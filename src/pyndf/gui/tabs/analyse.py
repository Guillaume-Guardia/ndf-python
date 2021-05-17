# -*- coding: utf-8 -*-

from pyndf.qtlib import QtWidgets
from pyndf.gui.tables.analyse import AnalyseTable


class AnalyseTab(QtWidgets.QWidget):
    def __init__(self, window, title, *args):
        super().__init__()
        self.window = window
        self.title = title

        # Create table
        self.table = AnalyseTable(self, *args)

        # Add table
        layout = QtWidgets.QHBoxLayout()
        layout.addWidget(self.table)
        self.setLayout(layout)
