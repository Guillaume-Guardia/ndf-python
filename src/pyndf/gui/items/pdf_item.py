# -*- coding: utf-8 -*-


from pyndf.gui.items.item import Item


class PDFItem(Item):
    """Class for storing data for analyse."""

    headers = ["filename", "total_db", "total", "nbr_missions", "status", "time"]

    def __init__(self, filename, total_db, total, nbr_missions, status, time):
        """Initialisation"""
        super().__init__()
        self.filename = filename
        self.total_db = total_db
        self.total = total
        self.nbr_missions = nbr_missions
        self.status = status
        self.time = time

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
