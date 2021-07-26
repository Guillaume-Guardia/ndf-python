# -*- coding: utf-8 -*-

from pyndf.process.reader.factory import Reader
from pyndf.qtlib import QtWidgets, QtGui, QtCore
from pyndf.constants import CONST


class MyScrollArea(QtWidgets.QScrollArea):
    def __init__(self, paths, ratio, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setCursor(QtCore.Qt.CursorShape.OpenHandCursor)
        self.last_time_move_x = 0
        self.last_time_move_y = 0
        self.ratio = ratio

        widget = QtWidgets.QWidget()
        widget.setLayout(self.create_layout(paths))
        self.setWidget(widget)
        self.setWidgetResizable(True)

    def wheelEvent(self, event):
        if event.modifiers() & QtCore.Qt.KeyboardModifier.ControlModifier:
            delta = event.angleDelta().y() / 360

            if delta > 0 and self.ratio < 5 or delta < 0 and self.ratio > 0.5:
                self.ratio += delta

            self.set_widget()
            return None

        super().wheelEvent(event)

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

    def mouseMoveEvent(self, event):
        self.setCursor(QtCore.Qt.CursorShape.ClosedHandCursor)
        # For x
        if self.last_time_move_x == 0:
            self.last_time_move_x = event.position().x()

        distance = self.last_time_move_x - event.position().x()
        self.horizontalScrollBar().setValue(self.horizontalScrollBar().value() + distance)
        self.last_time_move_x = event.position().x()

        # for y
        if self.last_time_move_y == 0:
            self.last_time_move_y = event.position().y()

        distance = self.last_time_move_y - event.position().y()
        self.verticalScrollBar().setValue(self.verticalScrollBar().value() + distance)
        self.last_time_move_y = event.position().y()

        return super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        self.setCursor(QtCore.Qt.CursorShape.OpenHandCursor)
        self.last_time_move_x = 0
        self.last_time_move_y = 0
        super().mouseReleaseEvent(event)


class PreviewDialog(QtWidgets.QDialog):
    def __init__(self, button, column):
        self.table = button.parent
        self.window = self.table.tab.window
        super().__init__(self.window)
        self.buttons = {}
        self.ratio = 3
        self.col = column
        self.row = 0

        # Window parameter
        self.setWindowFlag(QtCore.Qt.WindowType.WindowMinMaxButtonsHint, True)
        self.setWindowTitle(self.tr("PDF file viewer"))
        self.setSizeGripEnabled(True)
        self.setMinimumWidth(900)
        self.setMinimumHeight(700)

        # Add layout to view
        layout = QtWidgets.QVBoxLayout()

        # Container for the png view
        self.area = QtWidgets.QWidget()

        # Control layout
        self.control = self.create_control()

        # determine the row in table
        row = self.determine_row_in_table(button)

        layout.addWidget(self.area)
        layout.addLayout(self.control)
        self.setLayout(layout)

        self.render(row)

    def determine_row_in_table(self, item):
        items = self.table.findItems(item.path, QtCore.Qt.MatchFlag.MatchExactly)

        if len(items) > 0:
            return items[0].row()
        return 0

    def render(self, predicate):
        self.row += predicate
        if not (0 <= self.row < self.table.rowCount() - 1):
            return None

        # Png view
        png_paths = self.get_paths(self.row)
        if png_paths:
            area = MyScrollArea(png_paths, self.ratio)
            self.layout().replaceWidget(self.area, area)
            self.area.setParent(None)
            self.area = None
            self.area = area

    def get_paths(self, row):
        filename = self.table.cellWidget(row, self.col).path
        png_paths, status = Reader(
            filename, temp_dir=self.window.app.temp_dir, ratio=self.ratio, log_level=self.window.log_level
        )
        return png_paths

    def create_control(self):
        layout = QtWidgets.QHBoxLayout()

        layout.addStretch()
        self.buttons["left"] = QtWidgets.QPushButton(QtGui.QIcon(CONST.UI.ICONS.LEFT), "")
        self.buttons["left"].pressed.connect(lambda: self.render(-1))
        layout.addWidget(self.buttons["left"])

        layout.addStretch()
        self.buttons["right"] = QtWidgets.QPushButton(QtGui.QIcon(CONST.UI.ICONS.RIGHT), "")
        self.buttons["right"].pressed.connect(lambda: self.render(1))
        layout.addWidget(self.buttons["right"])

        layout.addStretch()
        return layout
