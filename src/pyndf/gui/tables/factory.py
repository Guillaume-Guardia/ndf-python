# -*- coding: utf-8 -*-

from pyndf.gui.tables.analyse import AnalyseTable
from pyndf.gui.tables.abstract import AbstractTable
from pyndf.gui.tables.excel import ExcelTable
from pyndf.gui.items.analyse.all_item import AllItem
from pyndf.gui.items.analyse.api_item import APIItem
from pyndf.gui.items.analyse.pdf_item import PDFItem
from pyndf.gui.items.reader.excel_item import ExcelItem
from pyndf.gui.tables.excel import ExcelTable


def tables_factory(tab, item):
    if item in (AllItem, APIItem, PDFItem):
        table = AnalyseTable
    elif item is ExcelItem:
        table = ExcelTable
    else:
        table = AbstractTable

    return table(tab, item)
