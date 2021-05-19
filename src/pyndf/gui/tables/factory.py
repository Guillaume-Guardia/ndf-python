# -*- coding: utf-8 -*-

from pyndf.gui.tables.useclass.analyse import AnalyseTable
from pyndf.gui.tables.abstract import AbstractTable
from pyndf.gui.tables.useclass.smart.excel import ExcelSmartTable
from pyndf.gui.items.useclass.analyse.all import AllItem
from pyndf.gui.items.useclass.analyse.api import ApiItem
from pyndf.gui.items.useclass.analyse.pdf import PdfItem
from pyndf.gui.items.useclass.reader.excel import ExcelItem


def tables_factory(tab, item):
    if item in (AllItem, ApiItem, PdfItem):
        table = AnalyseTable
    elif item is ExcelItem:
        table = ExcelSmartTable
    else:
        table = AbstractTable

    return table(tab, item)
