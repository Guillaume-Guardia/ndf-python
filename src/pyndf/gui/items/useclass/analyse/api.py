# -*- coding: utf-8 -*-


from pyndf.gui.items.abstract import AbstractItem
from pyndf.constants import CONST


class ApiItem(AbstractItem):
    """Class for storing data for analyse."""

    type = CONST.TYPE.API
    headers = ["matricule", "addr_client", "addr_employee", "distance", "status", "time"]

    @classmethod
    def headers_pretty(cls):
        # headers
        return [
            cls.tr("Matricule"),
            cls.tr("Client address"),
            cls.tr("Employee address"),
            cls.tr("Distance"),
            cls.tr("Status"),
            cls.tr("Time (s)"),
        ]
