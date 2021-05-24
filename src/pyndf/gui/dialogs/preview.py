# -*- coding: utf-8 -*-

import os
from pyndf.process.reader.factory import Reader
from pyndf.qtlib import QtWidgets, QtGui, QtCore
from pyndf.constants import CONST


class PreviewDialog(QtWidgets.QDialog):
    def __init__(self, window, filename):
        super().__init__(window)
        self.window = window

        self.setWindowFlag(QtCore.Qt.WindowType.WindowMinMaxButtonsHint, True)
        self.setWindowTitle(self.tr("PDF viewer"))
        self.setSizeGripEnabled(True)

        filename = os.path.join(window.output, filename + CONST.EXT.PDF)
        png_paths = Reader(filename, window, log_level=window.log_level)

        area = self.create_area(png_paths)
        layout = QtWidgets.QHBoxLayout()
        layout.addWidget(area)
        self.setLayout(layout)

    def create_area(self, paths):
        widget = QtWidgets.QWidget()
        widget.setLayout(self.create_layout(paths))
        widget.adjustSize()
        self.setMinimumWidth(widget.width())
        self.setMinimumHeight(widget.height())

        scroll_area = QtWidgets.QScrollArea()
        scroll_area.setWidget(widget)
        return scroll_area

    def create_layout(self, paths):
        layout = QtWidgets.QHBoxLayout()

        layout.addStretch()
        for path in paths:
            widget = self.create_widget(path)
            layout.addWidget(widget)
        layout.addStretch()
        return layout

    def create_widget(self, path):
        widget = QtWidgets.QLabel()
        pix = QtGui.QPixmap(path)
        widget.setPixmap(pix)
        widget.adjustSize()
        return widget
