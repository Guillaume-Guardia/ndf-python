# -*- coding: utf-8 -*-

from pyndf.constants import CONST
from pyndf.process.writer.useclass.csv import CsvWriter
from pyndf.process.writer.useclass.excel import ExcelWriter
from pyndf.process.writer.useclass.pdf import PdfWriter
from pyndf.utils import Factory


class Writer(Factory):
    class_dico = {
        CONST.TYPE.EXC: ExcelWriter,
        CONST.TYPE.CSV: CsvWriter,
        CONST.TYPE.PDF: PdfWriter,
    }
