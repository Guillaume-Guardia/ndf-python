# -*- coding: utf-8 -*-

from pyndf.constants import CONST
from pyndf.gui.items.useclass.reader.excel import ExcelItem


class GlobalExcelItem(ExcelItem):
    """Class for storing data for analyse."""

    type = CONST.TYPE.GLO_EXC
