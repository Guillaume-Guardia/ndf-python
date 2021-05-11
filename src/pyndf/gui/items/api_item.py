# -*- coding: utf-8 -*-


class APIItem:
    """Class for storing data for analyse."""

    def __init__(self, addr_client, addr_employee, distance, status, time):
        """Initialisation"""
        self.addr_client = addr_client
        self.addr_employee = addr_employee
        self.distance = distance
        self.status = status
        self.time = time

    @classmethod
    def headers(cls):
        # headers
        return ["addr_client", "addr_employee", "distance", "status", "time"]
