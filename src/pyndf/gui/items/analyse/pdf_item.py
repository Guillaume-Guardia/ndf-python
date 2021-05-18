# -*- coding: utf-8 -*-


from pyndf.gui.items.item import Item


class PDFItem(Item):
    """Class for storing data for analyse."""

    headers = ["filename", "total_db", "total", "nbr_missions", "status", "time"]

    @classmethod
    def headers_pretty(cls):
        # headers
        return [
            cls.tr("Filename"),
            cls.tr("DB Total"),
            cls.tr("Total"),
            cls.tr("Number of missions"),
            cls.tr("Status"),
            cls.tr("Time (s)"),
        ]
