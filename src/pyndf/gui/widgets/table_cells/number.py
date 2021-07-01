# -*- coding: utf-8 -*-

from pyndf.gui.widgets.table_cells.default import DefaultCellItem
from pyndf.qtlib import QtCore


class NumberCellItem(DefaultCellItem):
    """Class for storing data for analyse."""

    def __init__(self, value, colored, decimal=2):
        """Initialisation"""
        if isinstance(value, float):
            value = round(value, decimal)

        super().__init__(value, colored)

        self.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
