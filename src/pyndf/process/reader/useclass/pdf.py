# -*- coding: utf-8 -*-

import re
import fitz
from pyndf.constants import CONST
from pyndf.process.reader.abstract import AbstractReader
from pyndf.process.writer.factory import Writer


class PdfReader(AbstractReader):
    """Class for reading excel file."""

    type = CONST.TYPE.PDF
    regex = re.compile(".*[.]pdf")

    def read(self, filename=None, temp_dir=None, ratio=1):
        if self.check_path(filename) is False:
            return

        writer = Writer(CONST.TYPE.PNG, ratio=ratio, directory=temp_dir, log_level=self.log_level)

        # read pdf
        with fitz.Document(filename) as doc:
            paths = []
            for page in doc:  # iterate through the pages
                (filename, status), time_spend = writer.write(page, filename)
                paths.append(filename)

        return paths
