# -*- coding: utf-8 -*-

from pyndf.gui.items.useclass.analyse.all import AllItem
from pyndf.gui.items.useclass.analyse.api import ApiItem
from pyndf.gui.items.useclass.analyse.pdf import PdfItem
from pyndf.gui.items.useclass.analyse.total import TotalItem
from pyndf.gui.items.useclass.reader.excel import ExcelItem
from pyndf.gui.items.useclass.reader.csv import CsvItem
from pyndf.constants import CONST
from pyndf.utils import Factory


class Items(Factory):
    class_dico = {
        CONST.TYPE.ALL: AllItem,
        CONST.TYPE.API: ApiItem,
        CONST.TYPE.PDF: PdfItem,
        CONST.TYPE.EXC: ExcelItem,
        CONST.TYPE.CSV: CsvItem,
        CONST.TYPE.TOT: TotalItem,
    }
