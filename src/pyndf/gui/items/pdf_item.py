# -*- coding: utf-8 -*-


class PDFItem:
    """Class for storing data for analyse."""

    def __init__(self, filename, total_db, total, nbr_missions, status, time):
        """Initialisation"""
        self.filename = filename
        self.total_db = total_db
        self.total = total
        self.nbr_missions = nbr_missions
        self.status = status
        self.time = time

    @classmethod
    def headers(cls):
        # headers
        return ["filename", "total_db", "total", "nbr_missions", "status", "time"]
