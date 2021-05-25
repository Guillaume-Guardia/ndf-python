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

    def read(self, filename=None, window=None):
        if self.check_path(filename) is False:
            return

        writer = Writer(CONST.TYPE.PNG, directory=window.app.temp_dir)

        # read pdf
        with fitz.Document(filename) as doc:
            paths = []
            for page in doc:  # iterate through the pages
                paths.append(writer.write(page, filename))

        return paths
