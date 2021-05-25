# -*- coding: utf-8 -*-

import pandas as pd
from pyndf.constants import CONST
from pyndf.process.writer.abstract import AbstractWriter


class CsvWriter(AbstractWriter):
    """Class for writing csv file."""

    ext = CONST.EXT.CSV

    def _write(self, data, filename=None):
        df = pd.DataFrame(data)
        df.to_csv(filename, sep=";", decimal=",", index=False)
