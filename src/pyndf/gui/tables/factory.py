# -*- coding: utf-8 -*-

from pyndf.gui.tables.useclass.analyse import AnalyseTable
from pyndf.gui.tables.abstract import AbstractTable
from pyndf.gui.tables.useclass.smart.csv import CsvSmartTable
from pyndf.gui.tables.useclass.smart.excel import ExcelSmartTable
from pyndf.gui.items.useclass.analyse.all import AllItem
from pyndf.gui.items.useclass.analyse.api import ApiItem
from pyndf.gui.items.useclass.analyse.pdf import PdfItem
from pyndf.gui.items.useclass.reader.excel import ExcelItem
from pyndf.gui.items.useclass.reader.csv import CsvItem

map_item_table = {
    AllItem: AnalyseTable,
    ApiItem: AnalyseTable,
    PdfItem: AnalyseTable,
    ExcelItem: ExcelSmartTable,
    CsvItem: CsvSmartTable,
}


def tables_factory(tab, item):

    try:
        return map_item_table[item](tab, item)
    except KeyError:
        AbstractTable(tab, item)
