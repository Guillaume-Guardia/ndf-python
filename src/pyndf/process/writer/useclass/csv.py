# -*- coding: utf-8 -*-

import pandas as pd
from pyndf.process.writer.abstract import AbstractWriter


class CsvWriter(AbstractWriter):
    """Class for writing csv file."""

    ext = ".csv"

    def write(self, data, filename=None):
        path = self.create_path(filename)

        df = pd.DataFrame(data)
        df.to_csv(path, sep=";", decimal=",", index=False)

        return path
