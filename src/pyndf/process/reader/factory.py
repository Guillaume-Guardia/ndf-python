# -*- coding: utf-8 -*-

import re
from pyndf.process.reader.useclass.csv import CSVReader
from pyndf.process.reader.useclass.excel import ExcelReader

reader_regex = {
    ExcelReader: re.compile(".*[.][xX][lL]*"),
    CSVReader: re.compile(".*[.][cC][sS][vV]"),
}


def reader_factory(filename, *args, log_level=None, **kwargs):
    for reader, regex in reader_regex.items():
        if regex.match(filename):
            return reader(log_level=log_level).read(filename, *args, **kwargs)
    return None, None
