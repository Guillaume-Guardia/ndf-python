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

    def write(self, page, filename=None):
        path = self.create_path(filename, page=page.number)

        # pix = page.get_pixmap(matrix=self.mat, alpha=False)  # render page to an image
        pix = page.get_pixmap(alpha=False)
        pix.save(path)  # store image as a PNG

        return path
