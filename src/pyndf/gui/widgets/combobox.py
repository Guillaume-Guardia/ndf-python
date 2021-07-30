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

        # Add existed security
        self.activated.connect(self.check_path)

        self.view().pressed.connect(self.item_pressed)

        self.addItems(sorted(list(default)))

    def remove_item(self, filename):
        getattr(self.window, self.name_env).discard(filename)
        self.removeItem(self.currentIndex())

    def check_path(self, index=0):
        path = self.currentText()
        # Check if the path exists
        if not os.path.exists(path):
            QtWidgets.QMessageBox.information(
                self,
                self.tr("Path doesn't exist"),
                self.tr("The path {} doesn't exist! Choose another one!").format(path),
            )
            self.remove_item(path)
            return False
        return True

    def add_data(self, filename):
        self.window.tabs[self.name_env].table.init(filename=filename, clear=True)
        _, status = Reader(filename, analyse=self.window.tabs[self.name_env].table.add, log_level=self.window.log_level)
        if not status:
            QtWidgets.QMessageBox.information(
                self,
                self.tr("Cant read file"),
                self.tr("No reader implemented to open the file {}! Choose another file!").format(filename),
            )
            self.remove_item(filename)
        self.window.tabs[self.name_env].table.finished(bool(status))

    def add_items(self, paths):
        for path in paths:
            self.add_item(path)
            getattr(self.window, self.name_env).add(path)

    def add_item(self, path):
        if self.findText(path) == -1:
            self.addItem(path)
        self.setCurrentText(path)

    def item_pressed(self, model_index):
        """Method to delete item when click on right button of the mouse.

        Args:
            model_index (IndexModel): Item clicked
        """
        if QtGui.QGuiApplication.mouseButtons() == QtCore.Qt.MouseButton.RightButton:
            getattr(self.window, self.name_env).discard(self.itemText(model_index.row()))
            self.removeItem(model_index.row())
