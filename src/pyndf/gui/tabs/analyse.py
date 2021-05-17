# -*- coding: utf-8 -*-

from PyQt6 import QtCore, QtWidgets, QtGui
from pyndf.constants import CONFIG, COLORS
from pyndf.gui.items.total_item import TotalItem
from pyndf.gui.table.analyse import AnalyseTable


class AnalyseTab(QtWidgets.QWidget):
    def __init__(self, window, *args):
        super().__init__()
        self.window = window

        # Create table
        self.table = AnalyseTable(self, *args)

        # Add table
        layout = QtWidgets.QHBoxLayout()
        layout.addWidget(self.table)
        self.setLayout(layout)
