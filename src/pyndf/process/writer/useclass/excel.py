# -*- coding: utf-8 -*-

import pandas as pd
from pyndf.process.writer.abstract import AbstractWriter


class ExcelWriter(AbstractWriter):
    """Class for writing excel file."""

    ext = ".xlsx"
    engine = "xlsxwriter"

    def write(self, data, filename=None):
        path = self.create_path(filename)

        df = pd.DataFrame(data)

        with pd.ExcelWriter(path, engine=self.engine) as writer:
            df.to_excel(writer, index=False)

        return path
