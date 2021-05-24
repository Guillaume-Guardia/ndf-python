# -*- coding: utf-8 -*-

from markdown import markdown
from pyndf.qtlib import QtWidgets, QtGui, QtCore
from pyndf.constants import CONST


class ManualDialog(QtWidgets.QDialog):
    def __init__(self, parent):
        super().__init__(parent)
        self.setWindowFlag(QtCore.Qt.WindowType.WindowMinMaxButtonsHint, True)
        self.setWindowTitle(self.tr("Manual"))
        self.setSizeGripEnabled(True)
        self.setMinimumHeight(400)
        self.setMinimumWidth(400)

        right = self.create_right_widget()
        left = self.create_left_widget()

        layout = QtWidgets.QHBoxLayout()
        layout.addWidget(left)
        layout.addWidget(right)
        self.setLayout(layout)

    def create_left_widget(self):
        layout = QtWidgets.QVBoxLayout()

        # Title label
        title = QtWidgets.QLabel(f"{CONST.TITLE_APP}")
        title.setFont(QtGui.QFont(CONST.WRITER.PDF.FONT[0], 20))

        # Image
        image = QtWidgets.QLabel()
        pixmap = QtGui.QPixmap(CONST.FILE.LOGO)
        pixmap.scaledToWidth(50)
        image.setPixmap(pixmap)
        image.setScaledContents(False)

        # Version
        version = QtWidgets.QLabel(f"version: {CONST.VERSION}")

        # Add widget to layout
        layout.addWidget(title)
        layout.addWidget(image)
        layout.addWidget(version)

        widget = QtWidgets.QWidget()
        widget.setLayout(layout)

        return widget

    def create_manual_layout(self):
        layout = QtWidgets.QVBoxLayout()
        with open(CONST.FILE.README, encoding="utf-8") as opened_file:
            for line in opened_file.readlines():
                layout.addWidget(QtWidgets.QLabel(markdown(line)))

        return layout

    def create_right_widget(self):
        widget = QtWidgets.QWidget()
        widget.setLayout(self.create_manual_layout())

        scroll_area = QtWidgets.QScrollArea()
        scroll_area.setWidget(widget)

        return scroll_area
