# -*- coding: utf-8 -*-

from pyndf.process.writer.useclass.csv import CsvWriter
from pyndf.process.writer.useclass.excel import ExcelWriter
from pyndf.process.writer.useclass.pdf import PdfWriter
from pyndf.process.writer.abstract import AbstractWriter

from pyndf.gui.items.useclass.reader.excel import ExcelItem
from pyndf.gui.items.useclass.reader.csv import CsvItem


def writer_factory(item, *args, **kwargs):
    if item is ExcelItem:
        writer = ExcelWriter
    elif item is CsvItem:
        writer = CsvWriter
    else:
        writer = AbstractWriter

    return writer(item, *args, **kwargs)
