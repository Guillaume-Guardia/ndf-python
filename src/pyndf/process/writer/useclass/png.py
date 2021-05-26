# -*- coding: utf-8 -*-

import fitz
from pyndf.constants import CONST
from pyndf.process.writer.abstract import AbstractWriter


class PngWriter(AbstractWriter):
    """Class for writing csv file."""

    ext = CONST.EXT.PNG

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        zoom_x = 2.0  # horizontal zoom
        zomm_y = 2.0  # vertical zoom
        self.mat = fitz.Matrix(zoom_x, zomm_y)

    def _write(self, page, filename=None):
        # pix = page.get_pixmap(matrix=self.mat, alpha=False)  # render page to an image
        pix = page.get_pixmap(alpha=False)
        pix.save(filename)  # store image as a PNG

        return CONST.STATUS.OK
