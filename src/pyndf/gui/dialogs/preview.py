# -*- coding: utf-8 -*-

import os
from pyndf.process.reader.factory import Reader
from pyndf.qtlib import QtWidgets, QtGui, QtCore
from pyndf.constants import CONST


class PreviewDialog(QtWidgets.QDialog):
    def __init__(self, table, col, row):
        super().__init__(table.tab.window)
        self.table = table
        self.row = row
        self.window = table.tab.window
        self.buttons = {}
        self.col = col

        self.setWindowFlag(QtCore.Qt.WindowType.WindowMinMaxButtonsHint, True)
        self.setWindowTitle(self.tr("PDF file viewer"))
        self.setSizeGripEnabled(True)

        self.render(row)

    def render(self, row):
        if not (0 <= row < self.table.rowCount() - 1):
            return None

        if self.layout():
            layout = self.layout()
            # Remove all child item

            while layout.takeAt(0):
                child = layout.takeAt(0)
                del child
        else:
            layout = QtWidgets.QVBoxLayout()

        # Layout view
        png_paths = self.get_paths(row)
        if png_paths:
            area = self.create_area(png_paths)
            layout.addWidget(area)

        control = self.create_control()
        layout.addLayout(control)
        self.setLayout(layout)

    def get_paths(self, row):
        self.row = row
        filename = self.table.item(row, self.col).text()
        png_paths = Reader(filename, self.window, log_level=self.window.log_level)

        return png_paths

    def create_control(self):
        layout = QtWidgets.QHBoxLayout()

        layout.addStretch()
        self.buttons["left"] = QtWidgets.QPushButton(QtGui.QIcon(CONST.UI.ICONS.LEFT), "")
        self.buttons["left"].pressed.connect(lambda: self.render(self.row - 1))
        layout.addWidget(self.buttons["left"])

        layout.addStretch()
        self.buttons["right"] = QtWidgets.QPushButton(QtGui.QIcon(CONST.UI.ICONS.RIGHT), "")
        self.buttons["right"].pressed.connect(lambda: self.render(self.row + 1))
        layout.addWidget(self.buttons["right"])

        layout.addStretch()
        return layout

    def create_area(self, paths):
        widget = QtWidgets.QWidget()
        widget.setLayout(PreviewDialog.create_layout(paths))
        widget.adjustSize()
        self.setMinimumWidth(widget.width())
        self.setMinimumHeight(widget.height())

        scroll_area = QtWidgets.QScrollArea()
        scroll_area.setWidget(widget)
        return scroll_area

    @staticmethod
    def create_layout(paths):
        layout = QtWidgets.QHBoxLayout()

        layout.addStretch()
        for path in paths:
            widget = PreviewDialog.create_widget(path)
            layout.addWidget(widget)
        layout.addStretch()
        return layout

    @staticmethod
    def create_widget(path):
        widget = QtWidgets.QLabel()
        pix = QtGui.QPixmap(path)
        widget.setPixmap(pix)
        widget.adjustSize()
        return widget
