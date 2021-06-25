# -*- coding: utf-8 -*-

from pyndf.qtlib import QtWidgets, QtCore


class ControlButtons(QtWidgets.QWidget):
    def __init__(self, windows, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.windows = windows

        self.buttons = {}

        # Create vertical layout
        layout = QtWidgets.QHBoxLayout()

        # Cancel button
        icon = ""  # TODO find icon pause

        text = self.tr("&Cancel")  # Alt + C
        self.buttons["cancel"] = QtWidgets.QPushButton(text, parent=self)
        self.buttons["cancel"].clicked.connect(self.cancel)

        layout.addWidget(self.buttons["cancel"])

        self.setLayout(layout)

    def cancel(self):
        if self.windows.process is not None:
            self.windows.process.flags.cancel = True
