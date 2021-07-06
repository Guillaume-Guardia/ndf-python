# -*- coding: utf-8 -*-

from pyndf.process.reader.factory import Reader
from pyndf.qtlib import QtWidgets, QtGui, QtCore
from pyndf.constants import CONST


class PreviewDialog(QtWidgets.QDialog):
    def __init__(self, table, row, col):
        super().__init__(table.tab.window)
        self.table = table
        self.row = row
        self.window = table.tab.window
        self.buttons = {}
        self.col = col
        self.ratio = 3

        self.setWindowFlag(QtCore.Qt.WindowType.WindowMinMaxButtonsHint, True)
        self.setWindowTitle(self.tr("PDF file viewer"))
        self.setSizeGripEnabled(True)
        self.setMinimumWidth(900)
        self.setMinimumHeight(700)

        self.render(row)

    def render(self, row):
        if not (0 <= row < self.table.rowCount() - 1):
            return None

        if self.layout():
            layout = self.layout()
            # Remove all child item

            while layout.takeAt(0):
                child = layout.takeAt(0)
                if child:
                    child.deleteLater()
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
        filename = self.table.cellWidget(row, self.col).path
        png_paths, status = Reader(
            filename, temp_dir=self.window.app.temp_dir, ratio=self.ratio, log_level=self.window.log_level
        )

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
        scroll_area = QtWidgets.QScrollArea()
        widget = QtWidgets.QWidget()
        widget.setLayout(self.create_layout(paths))
        scroll_area.setWidget(widget)
        scroll_area.setWidgetResizable(True)
        return scroll_area

    def create_layout(self, paths):
        layout = QtWidgets.QHBoxLayout()
        layout.addStretch()
        for path in paths:
            layout.addWidget(self.set_widget(path))
        layout.addStretch()
        return layout

    def set_widget(self, path=None):
        if path is not None:
            self.widget = QtWidgets.QLabel()
            self.pix = QtGui.QPixmap(path)
        self.pix.setDevicePixelRatio(self.ratio)
        self.widget.setPixmap(self.pix)
        return self.widget

    def wheelEvent(self, event):
        self.ratio += event.angleDelta().y() / 360

        if event.modifiers() & QtCore.Qt.KeyboardModifier.ControlModifier:
            self.set_widget()
