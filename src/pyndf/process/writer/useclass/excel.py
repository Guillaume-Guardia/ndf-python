# -*- coding: utf-8 -*-

import pandas as pd
from pyndf.constants import CONST
from pyndf.process.writer.abstract import AbstractWriter


class ExcelWriter(AbstractWriter):
    """Class for writing excel file."""

    ext = CONST.EXT.EXC
    engine = "xlsxwriter"

    def _write(self, data, filename=None):
        df = pd.DataFrame(data)
        with pd.ExcelWriter(filename, engine=self.engine) as writer:
            df.to_excel(writer, index=False)
