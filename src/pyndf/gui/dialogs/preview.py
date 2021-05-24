# -*- coding: utf-8 -*-

import os
from pyndf.process.reader.factory import Reader
from pyndf.qtlib import QtWidgets, QtGui, QtCore
from pyndf.constants import CONST


class PreviewDialog(QtWidgets.QDialog):
    def __init__(self, table, row):
        super().__init__(table.tab.window)
        self.table = table
        self.row = row
        self.window = table.tab.window
        self.buttons = {}

        self.pdf_widget = None

        self.setWindowFlag(QtCore.Qt.WindowType.WindowMinMaxButtonsHint, True)
        self.setWindowTitle(self.tr("PDF viewer"))
        self.setSizeGripEnabled(True)

        self.render(row)

    def render(self, row):
        if not (0 <= row < self.table.rowCount() - 1):
            return None

        # Layout view
        area = self.create_area(self.get_paths(row))
        control = self.create_control()

        if self.layout():
            layout = self.layout()
            # Remove all child item

            while layout.takeAt(0):
                child = layout.takeAt(0)
                del child
        else:
            layout = QtWidgets.QVBoxLayout()
        layout.addWidget(area)
        layout.addLayout(control)
        self.setLayout(layout)

    def get_paths(self, row):
        self.row = row
        filename = self.table.item(row, 0).text()
        path = os.path.join(self.window.output, filename + CONST.EXT.PDF)
        png_paths = Reader(path, self.window, log_level=self.window.log_level)

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
