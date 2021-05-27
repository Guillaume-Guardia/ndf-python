# -*- coding: utf-8 -*-

from pyndf.qtlib import QtWidgets, QtGui, QtCore
from pyndf.constants import CONST


class AbstractItem(QtCore.QObject):
    """Class for storing data for analyse."""

    font = "Helvetica [Cronyx]"
    font_size = 11
    font_weight = QtGui.QFont.Weight.Bold
    headers = []

    def __init__(self, *args, columns=None, colored=False):
        """Initialisation"""
        super().__init__()
        self.colored = colored

        if columns is not None:
            self.headers = list(columns)

        for index, arg in enumerate(args):
            setattr(self, self.headers[index], arg)

        self.counter = len(args)

    def __setattr__(self, name: str, value) -> None:
        if isinstance(value, list) or name in ("counter", "colored"):
            return super().__setattr__(name, value)

        if name == "time":
            edit_value = round(value, 4)
        elif isinstance(value, float):
            edit_value = round(value, 2)
        elif name == "status":
            edit_value = str(value)
        else:
            edit_value = value

        widget = QtWidgets.QTableWidgetItem()
        widget.setData(QtCore.Qt.ItemDataRole.EditRole, edit_value)

        if name == "status" or isinstance(value, (int, float)):
            widget.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        if name == "status":
            widget.setFont(QtGui.QFont(self.font, self.font_size, self.font_weight))
            widget.setForeground(QtGui.QColor(value.color))

        if self.colored:
            widget.setBackground(QtGui.QColor(CONST.WRITER.PDF.COLOR))
        super().__setattr__(name, widget)

    def __iter__(self):
        for name in self.headers:
            yield name, getattr(self, name)
