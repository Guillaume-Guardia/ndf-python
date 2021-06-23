# -*- coding: utf-8 -*-

from pyndf.constants import CONST
from pyndf.gui.items.abstract import AbstractItem
from pyndf.db.client import Client


class ClientItem(AbstractItem):
    """Class for storing data for analyse."""

    type = CONST.TYPE.DB_CLIENT
    db_class = Client
    headers = ["id", "name", "address"]

    def __init__(self, obj):
        """Initialisation"""
        super().__init__()

        for header in self.headers:
            setattr(self, header, getattr(obj, header))

    @classmethod
    def headers_pretty(cls):
        # headers
        return cls.headers
