# -*- coding: utf-8 -*-

from pyndf.qtlib import QtWidgets, QtCore, QtGui
from pyndf.constants import CONST


class DefaultCellItem(QtWidgets.QTableWidgetItem):
    """Class for storing data for analyse."""

    def __init__(self, value="", colored=False):
        """Initialisation"""
        super().__init__(type=1001)

        self.setData(QtCore.Qt.ItemDataRole.EditRole, value)

        if colored:
            self.setBackground(QtGui.QColor(CONST.WRITER.PDF.COLOR))

    def update_mode(self, dev_mode):
        pass
