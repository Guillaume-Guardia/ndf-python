# -*- coding: utf-8 -*-

from pyndf.qtlib import QtWidgets, QtGui, QtCore


class StatusCellItem(QtWidgets.QTableWidgetItem):
    """Class for storing data for analyse."""

    font = "Helvetica [Cronyx]"
    font_size = 11
    font_weight = QtGui.QFont.Weight.Bold

    def __init__(self, status_obj):
        """Initialisation"""
        super().__init__(type=1001)
        self.status = status_obj

        self.setFont(QtGui.QFont(self.font, self.font_size, self.font_weight))
        self.setForeground(QtGui.QColor(status_obj.color))
        self.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.setIcon(QtGui.QIcon(status_obj.icon))

    def update_mode(self, dev_mode):
        if dev_mode:
            self.setText(str(self.status))
        else:
            self.setText("")
