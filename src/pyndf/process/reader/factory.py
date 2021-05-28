# -*- coding: utf-8 -*-

from pyndf.process.reader.useclass.csv import CsvReader
from pyndf.process.reader.useclass.excel import ExcelReader
from pyndf.process.reader.useclass.pdf import PdfReader
from pyndf.utils import Factory
from pyndf.constants import CONST


class Reader(Factory):
    class_list = [ExcelReader, CsvReader, PdfReader]

    def __new__(cls, filename, *args, log_level=None, **kwargs):
        for reader in cls.class_list:
            if reader.can_read(filename):
                instance = reader.__new__(reader, log_level=log_level)
                instance.__init__(log_level=log_level)
                return instance.read(filename, *args, **kwargs), CONST.STATUS.OK
        return {}, CONST.STATUS.CANT_READ
