# -*- coding: utf-8 -*-

from pyndf.gui.tables.analyse import AnalyseTable
from pyndf.gui.tables.abstract import AbstractTable
from pyndf.gui.items.analyse.all_item import AllItem
from pyndf.gui.items.analyse.api_item import APIItem
from pyndf.gui.items.analyse.pdf_item import PDFItem


def tables_factory(tab, item):
    if item in (AllItem, APIItem, PDFItem):
        return AnalyseTable(tab, item)
    return AbstractTable(tab, item)
