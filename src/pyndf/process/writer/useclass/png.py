# -*- coding: utf-8 -*-

import fitz
from pyndf.constants import CONST
from pyndf.process.writer.abstract import AbstractWriter


class PngWriter(AbstractWriter):
    """Class for writing csv file."""

    ext = CONST.EXT.PNG

    def __init__(self, *args, ratio=1, **kwargs):
        super().__init__(*args, **kwargs)
        self.mat = fitz.Matrix(ratio, ratio)

    def _write(self, page, filename=None):
        pix = page.get_pixmap(matrix=self.mat, alpha=False)  # render page to an image
        pix.save(filename)  # store image as a PNG

        return CONST.STATUS.OK
