# -*- coding: utf-8 -*-


from pyndf.gui.items.abstract import AbstractItem
from pyndf.constants import CONST


class PdfItem(AbstractItem):
    """Class for storing data for analyse."""

    type = CONST.TYPE.PDF
    headers = ["matricule", "filename", "name", "nbr_missions", "nbr_indemnites", "status", "time", "retry"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Special case for the retry button
        self.counter += 1

    @classmethod
    def headers_pretty(cls):
        # headers
        return [
            cls.tr("Matricule"),
            cls.tr("Filename"),
            cls.tr("Name"),
            cls.tr("Number of missions"),
            cls.tr("Number of indemnity"),
            cls.tr("Status"),
            cls.tr("Time (s)"),
            cls.tr("Retry"),
        ]
