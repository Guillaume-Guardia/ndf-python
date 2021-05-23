# -*- coding: utf-8 -*-

from pyndf.qtlib import QtWidgets


class AbstractTab(QtWidgets.QWidget):
    def __init__(self, window, title):
        super().__init__()
        self.window = window
        self.title = title
