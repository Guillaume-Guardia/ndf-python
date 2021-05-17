# -*- coding: utf-8 -*-

from pyndf.qtlib import QtWidgets, QtGui, QtCore
from pyndf.constants import COLORS


class Item(QtCore.QObject):
    """Class for storing data for analyse."""

    font = "Helvetica [Cronyx]"
    font_size = 11
    font_weight = QtGui.QFont.Weight.Bold
    headers = []

    @classmethod
    def column_count(cls):
        return len(cls.headers)

    def __setattr__(self, name: str, value) -> None:
        if name == "time":
            value = round(value, 4)
        elif isinstance(value, float):
            value = round(value, 2)

        widget = QtWidgets.QTableWidgetItem(str(value))

        if name == "status" or isinstance(value, (int, float)):
            widget.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        if name == "status":
            widget.setFont(QtGui.QFont(self.font, self.font_size, self.font_weight))
            widget.setForeground(QtGui.QColor(COLORS.get(value, COLORS["others"])))
        super().__setattr__(name, widget)

    def __iter__(self):
        for name in self.headers:
            yield name, getattr(self, name)
