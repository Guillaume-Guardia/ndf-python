# -*- coding: utf-8 -*-


class AllItem:
    """Class for storing data for analyse."""

    def __init__(self, name, status, time):
        """Initialisation"""
        self.name = name
        self.status = status
        self.time = time

    @classmethod
    def headers(cls):
        # headers
        return ["name", "status", "time"]
