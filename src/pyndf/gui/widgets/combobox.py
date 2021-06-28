# -*- coding: utf-8 -*-

import os
from pyndf.qtlib import QtWidgets, QtGui, QtCore
from pyndf.constants import CONST
from pyndf.process.reader.factory import Reader


class FileSelectComboBox(QtWidgets.QComboBox):
    def __init__(self, window, name_env, default):
        super().__init__()
        self.window = window
        self.name_env = name_env

        self.setFixedHeight(30)
        self.setEditable(False)  # must use the file finder to select a valid file.

        if name_env in CONST.TAB.READER:
            self.currentTextChanged.connect(self.add_data)

        self.view().pressed.connect(self.item_pressed)

        self.addItems(sorted(list(default)))

    def add_data(self, filename):
        self.window.tabs[self.name_env].table.init(clear=True)
        _, status = Reader(filename, analyse=self.window.tabs[self.name_env].table.add, log_level=self.window.log_level)
        if not status:
            QtWidgets.QMessageBox.information(
                self,
                self.tr("Cant read file"),
                self.tr("No reader implemented to open the file {}! Choose another file!").format(filename),
            )
            getattr(self.window, self.name_env).discard(filename)
            self.removeItem(self.currentIndex())
        self.window.tabs[self.name_env].table.finished(bool(status))

    def add_items(self, paths):
        for path in paths:
            if path not in getattr(self.window, self.name_env):
                self.addItem(path)
                self.setCurrentText(path)

            getattr(self.window, self.name_env).add(path)

    def item_pressed(self, model_index):
        """Method to delete item when click on right button of the mouse.

        Args:
            model_index (IndexModel): Item clicked
        """
        if QtGui.QGuiApplication.mouseButtons() == QtCore.Qt.MouseButton.RightButton:
            getattr(self.window, self.name_env).discard(self.itemText(model_index.row()))
            self.removeItem(model_index.row())
