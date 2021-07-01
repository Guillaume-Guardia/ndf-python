# -*- coding: utf-8 -*-

from pyndf.qtlib import QtCore
from pyndf.gui.widgets.table_cells.status import StatusCellItem
from pyndf.gui.widgets.table_cells.default import DefaultCellItem
from pyndf.gui.widgets.table_cells.number import NumberCellItem


class AbstractItem(QtCore.QObject):
    """Class for storing data for analyse."""

    headers = []

    def __init__(self, *args, columns=None, colored=False):
        """Initialisation"""
        super().__init__()
        self.colored = colored

        if columns is not None:
            self.headers = list(columns)

        for header, arg in zip(self.headers, args):
            setattr(self, header, arg)

        self.counter = len(args)

    def __setattr__(self, name: str, value) -> None:
        if isinstance(value, list) or name in ("counter", "colored", "filename"):
            pass
        elif name == "status":
            value = StatusCellItem(value)
        elif name == "time":
            value = NumberCellItem(value, self.colored, 4)
        elif isinstance(value, (int, float)):
            value = NumberCellItem(value, self.colored)
        else:
            value = DefaultCellItem(value, self.colored)

        super().__setattr__(name, value)

    def __iter__(self):
        for name in self.headers:
            yield name, getattr(self, name, DefaultCellItem())
