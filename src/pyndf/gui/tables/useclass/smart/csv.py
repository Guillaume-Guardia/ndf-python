# -*- coding: utf-8 -*-

from pyndf.constants import CONST
from pyndf.gui.tables.useclass.smart.abstract import AbstractSmartTable


class CsvSmartTable(AbstractSmartTable):
    type = CONST.TYPE.CSV
