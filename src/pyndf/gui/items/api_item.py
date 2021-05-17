# -*- coding: utf-8 -*-


from pyndf.gui.items.item import Item


class APIItem(Item):
    """Class for storing data for analyse."""

    headers = ["addr_client", "addr_employee", "distance", "status", "time"]

    def __init__(self, addr_client, addr_employee, distance, status, time):
        """Initialisation"""
        super().__init__()
        self.addr_client = addr_client
        self.addr_employee = addr_employee
        self.distance = distance
        self.status = status
        self.time = time

    @classmethod
    def headers_pretty(cls):
        # headers
        return [
            cls.tr("Client address"),
            cls.tr("Employee address"),
            cls.tr("Distance"),
            cls.tr("Status"),
            cls.tr("Time (s)"),
        ]
