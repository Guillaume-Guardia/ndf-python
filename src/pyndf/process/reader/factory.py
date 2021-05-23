# -*- coding: utf-8 -*-

from pyndf.process.reader.useclass.csv import CSVReader
from pyndf.process.reader.useclass.excel import ExcelReader
from pyndf.utils import Factory


class Reader(Factory):
    class_list = [ExcelReader, CSVReader]

    def __new__(cls, filename, *args, log_level=None, **kwargs):
        instance = None, None
        for reader in cls.class_list:
            if reader.can_read(filename):
                instance = reader.__new__(reader, log_level=log_level)
                instance.__init__()
                return instance.read(filename, *args, **kwargs)
        return instance
