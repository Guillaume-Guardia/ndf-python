# -*- coding: utf-8 -*-

from pyndf.qtlib import QtWidgets
from pyndf.gui.tabs.abstract import AbstractTab
from pyndf.gui.tables.factory import Table


class AnalyseTab(AbstractTab):
    def __init__(self, window, title, item):
        super().__init__(window, title)

        # Create table
        self.table = Table(item.type, self, item)

        # Add table
        layout = QtWidgets.QHBoxLayout()
        layout.addWidget(self.table)
        self.setLayout(layout)
