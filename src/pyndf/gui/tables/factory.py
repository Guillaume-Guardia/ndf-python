# -*- coding: utf-8 -*-

from pyndf.utils import Factory
from pyndf.gui.tables.useclass.analyse import AnalyseTable
from pyndf.gui.tables.useclass.pdf import PdfTable
from pyndf.gui.tables.useclass.smart.csv import CsvSmartTable
from pyndf.gui.tables.useclass.smart.excel import ExcelSmartTable
from pyndf.constants import CONST


class Table(Factory):
    class_dico = {
        CONST.TYPE.ALL: AnalyseTable,
        CONST.TYPE.API: AnalyseTable,
        CONST.TYPE.PDF: PdfTable,
        CONST.TYPE.EXC: ExcelSmartTable,
        CONST.TYPE.CSV: CsvSmartTable,
    }
